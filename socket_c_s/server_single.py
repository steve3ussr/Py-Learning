from socket import *
import time


class Server:
    def __init__(self, port=13000, name=str(time.time())):
        self.port = port
        self.name = name
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('127.0.0.1', self.port))
        self.socket.listen(1)

        print(f"server({self.name}) is LISTENING.")

    @classmethod
    def _convert(cls, sentence):
        return sentence.upper()

    def _exec(self):

        while True:
            cli_socket, cli_addr = self.socket.accept()
            print(f'server({self.name}) is ACCEPT, client @ {cli_addr}.')

            while True:

                sentence = cli_socket.recv(1024).decode()
                if not sentence or sentence.lower().strip() == 'quit':
                    break

                res = self._convert(sentence)

                print(f"server({self.name}) recv: {cli_addr}, {sentence} --> {res}")
                cli_socket.send(res.encode())

            print(f'server({self.name}) closed, LISTENING NOW.')
            cli_socket.close()

    def start(self):
        while True:
            try:
                self._exec()
            except ConnectionResetError:
                print(f"Connect reset.")


if __name__ == '__main__':
    svr = Server(name='new_test_server')
    svr.start()
