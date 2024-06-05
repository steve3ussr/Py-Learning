from socket import *
import time
from client import Client


class ClientMock:
    def __init__(self, name=str(time.time()), tasks=()):
        self.name = name
        self.svr_addr = '127.0.0.1'
        self.svr_port = 13000
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.tasks = tasks

    def _connect(self):
        try:
            self.socket.connect((self.svr_addr, self.svr_port))
            print(f"{self.name} connected. (self: {self.socket})")
        except ConnectionRefusedError:
            print(f'Client({self.name}) cannot connect to server ({self.svr_addr} @ {self.svr_port})')
            raise

    def _exec(self):
        for interval, sentence in self.tasks:
            self.socket.send(sentence.encode())
            print(f'Client({self.name}) send: {sentence}')
            if sentence.lower().strip() == 'quit':
                break

            res = self.socket.recv(1024)
            print(f"From server to {self.name}:   {res.decode()}")
            time.sleep(interval)

    def start(self):
        try:
            self._connect()
            self._exec()
        except ConnectionRefusedError:
            print('Connect Error!')
        except Exception as e:
            print(f"Unexpected Error: {e.args}")
        finally:
            print(f'Client({self.name}) closed. ')


if __name__ == '__main__':
    client = Client('new_client')
    client.start()
