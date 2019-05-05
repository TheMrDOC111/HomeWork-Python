import asyncore
import asynchat
import logging
import mimetypes
import os
from urllib.parse import urlparse, unquote
from time import strftime, gmtime
import email
import re
from io import StringIO


def url_normalize(path):
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1 + 3:]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = unquote(path)
    return path


class FileProducer(object):

    def __init__(self, file, chunk_size=4096):
        self.file = file
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ""


class AsyncServer(asyncore.dispatcher):

    def __init__(self, host="127.0.0.1", port=9000, handler_class=None):
        super().__init__()
        self.handler_class = handler_class
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, address):
        logging.debug(f"Incoming connection from {address}")
        self.handler_class(sock)

    def serve_forever(self):
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            logging.debug("Worker shutdown")
        finally:
            self.close()


class AsyncHTTPRequestHandler(asynchat.async_chat):

    def __init__(self, sock):
        super().__init__(sock)
        self.ibuffer = ''
        self.obuffer = b''
        self.set_terminator(b'\r\n\r\n')
        self.reading_headers = True
        self.request = ''
        self.headers = {}
        self.response = ''

    def collect_incoming_data(self, data):
        if not self.reading_headers:
            self.obuffer = data
        else:
            self.ibuffer += data.decode('utf-8')

    def found_terminator(self):
        self.parse_request()

    def parse_request(self):
        if self.reading_headers:
            self.reading_headers = False
            request, headers = self.ibuffer.split('\r\n', 1)
            self.parse_headers(headers)
            self.headers['method'], self.headers['path'], self.headers['protocol'] = request.split()
            if self.headers['method'] == 'POST':
                clen = self.headers['Content-Length']
                print(self.headers)
                if clen == '0':
                    print(clen)
                    self.send_error(400)
                    return
                self.set_terminator(int(clen))
            else:
                self.request = urlparse('http://' + self.headers['Host'] + self.headers['path']).path
                self.ibuffer = ''
                self.handle_request()
        else:
            self.request = urlparse('http://' + self.headers['Host'] + self.headers['path']).path
            self.ibuffer = ''
            self.handle_request()

    def parse_headers(self, headers):
        message = email.message_from_file(StringIO(headers))
        self.headers = dict(message.items())

    def handle_request(self):
        method_name = 'do_' + self.headers['method']
        if not hasattr(self, method_name):
            self.send_error(405)
            return
        handler = getattr(self, method_name)
        handler()

    def init_response(self, code, message=None):
        self.response = f'HTTP/1.1 {code} {message}\r\n'

    def add_header(self, keyword, value):
        self.response += f"{keyword}: {value}\r\n"

    def end_headers(self):
        self.response += "\r\n"

    def send_error(self, code, message=None):
        print(code, self.headers)
        try:
            short_msg, long_msg = self.responses[code]
        except KeyError:
            short_msg, long_msg = '???', '???'
        if message is None:
            message = short_msg
        self.init_response(code, message)
        self.add_header("Content-Type", "text/plain")
        self.add_header("Connection", "close")
        self.end_headers()
        self.send(bytes(self.response.encode('utf-8')))
        self.close()

    def send_head(self):
        path = url_normalize(os.getcwd() + self.request)
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
            if not os.path.exists(path):
                self.send_error(403)
                return None
        try:
            file = bytes()
            fp = FileProducer(open(path, 'rb'))
            while True:
                cur_chunk = fp.more()
                if not cur_chunk:
                    break
                file += cur_chunk
        except IOError:
            self.send_error(404)
            return None

        _, ext = os.path.splitext(path)
        ctype = mimetypes.types_map[ext.lower()]

        self.init_response(200)
        self.add_header("Server", "server")
        self.add_header("Content-Type", ctype)
        self.add_header("Content-Length", os.path.getsize(path))
        self.end_headers()
        return file

    def do_GET(self):
        f = self.send_head()
        if f:
            resp = bytes(self.response.encode('utf-8')) + f
            self.send(resp)
            self.close()

    def do_HEAD(self):
        f = self.send_head()
        if f:
            resp = bytes(self.response.encode('utf-8'))
            self.send(resp)
            self.close()

    def do_POST(self):
        self.init_response(200, "OK")
        self.add_header("Content-Type", self.headers['Content-Type'])
        self.add_header("Connection", "close")
        self.add_header("Content-Length", self.headers['Content-Length'])
        self.end_headers()
        resp = bytes(self.response.encode('utf-8')) + self.obuffer
        self.send(resp)
        self.close()

    responses = {
        200: ('OK', 'Request fulfilled, document follows'),
        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
    }


def run():
    server = AsyncServer(host="127.0.0.1", port=9000, handler_class=AsyncHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
