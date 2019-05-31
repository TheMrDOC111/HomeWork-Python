import socket
from threading import Thread
import threading
import dispy


class Server:

    def get_socket(self):
        while True:
            print("Ожидание пользователя...")
            client, addr = sock.accept()
            clients.append({"connection": client, "socket": addr})
            print("connected:", addr)
            Thread(target=self.check_messages, args=(client,)).start()

    def check_messages(self, client):
        while True:
            try:
                data = client.recv(2048)
                data = str(data.decode("utf-8"))
                print("Data is", data)
                if len(data) == 0:
                    self.delete_user_socket(client)
                self.cast(client, data)
            except Exception as ex:
                print(ex)
                self.delete_user_socket(client)
                break

    def delete_user_socket(self, client):
        for user in clients:
            if user["connection"] == client:
                clients.remove(user)
                print("Пользователь удалён", client)
                break

    def broadcast(self, message: str):
        message += "\n"
        for user in clients:
            user["connection"].send(message.encode())

    def cast(self, client, n):
        print(n)
        self.banchmark(int(n))
        message = "EZ"
        message += "\n"
        client.send(message.encode())

    def __init__(self):
        sock.bind(('', 9090))
        sock.listen(10)
        print("Сервер запущен на сокете:", sock)

    def banchmark(self, n):
        cluster = dispy.JobCluster(compute)
        jobs = []
        for i in range(n):
            job = cluster.submit(100000000)
            job.id = i
            jobs.append(job)
        for job in jobs:
            host, n = job()
            print('%s executed job %s at %s with %s' % (host, job.id, job.start_time, n))
        cluster.print_status()
        return "EZ"


def compute(n):
    k = 2 ** n
    host = socket.gethostname()
    return host, "DONE"


if __name__ == "__main__":
    sock = socket.socket()
    clients = []
    server = Server()

    thread = threading.Thread(target=server.get_socket())
    thread.start()
    thread.join()
    sock.close()
    print("Server close")
