import asyncore
import asynchat


class AsyncHTTPRequestHandler(asynchat.async_chat):

    def __init__(self, sock):
        super().__init__(sock)
        self.set_terminator(b"\r\n\r\n")

    def collect_incoming_data(self, data):
        print(f"Incoming data: {data}")
        self.push(data)
        self._collect_incoming_data(data)

    def push(self, data):
        super().push(data)

    def found_terminator(self):
        self.parse_request()

    def parse_request(self):
        pass

    def parse_headers(self):
        pass


class AsyncHTTPServer(asyncore.dispatcher):

    def __init__(self, host="127.0.0.1", port=9000):
        super().__init__()
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print(f"Incoming connection from {addr}")
        AsyncHTTPRequestHandler(sock)


server = AsyncHTTPServer()
asyncore.loop()
