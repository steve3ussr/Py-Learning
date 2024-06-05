from socket import *
import time


class Client:
    def __init__(self, name=str(time.time())):
        self.name = name
        self.svr_addr = '127.0.0.1'
        self.svr_port = 13000
        self.socket = socket(AF_INET, SOCK_STREAM)

    def _connect(self):
        try:
            self.socket.connect((self.svr_addr, self.svr_port))
        except ConnectionRefusedError:
            print(f'Client cannot connect to server ({self.svr_addr} @ {self.svr_port})')
            raise

    def _exec(self):
        while True:
            sentence = input("enter single-line string: ")
            self.socket.send(sentence.encode())

            if sentence.lower().strip() == 'quit':
                break

            res = self.socket.recv(1024)
            print(f"From server:   {res.decode()}")

    def start(self):
        try:
            self._connect()
            self._exec()
        except ConnectionRefusedError:
            print('Connect Error!')
        finally:
            print(f'Client({self.name}) closed. ')


if __name__ == '__main__':
    client = Client('new_client')
    client.start()
