from socket import *
import time
from client import Client


class ClientMock(Client):
    def __init__(self, name=str(time.time()), tasks=()):
        super().__init__(name)
        self.tasks = tasks

    def _exec(self):
        for interval, message in self.tasks:

            if message.lower().strip() == 'quit':
                break

            if message and message[-1] != '\n':
                message += '\n'

            self.socket.send(message.encode())
            res = self.socket.recv(1024)
            # print(f"From server to {self.name}:  {message} --> {res.decode()}")

            time.sleep(interval)


if __name__ == '__main__':
    client = Client('new_client')
    client.start()
