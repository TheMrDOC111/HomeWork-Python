import socket
import time

sock = socket.socket()
sock.connect(('localhost', 9090))
sock.send(b"15")
data = sock.recv(1024)
print(data, "CLOSE")
time.sleep(1000)
sock.close()
