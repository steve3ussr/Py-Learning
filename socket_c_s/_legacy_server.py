# server
from socket import *

serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('the serveris ready to recv.')

while True:
    connectionSocket, addr = serverSocket.accept()
    print('received: ACCEPT')

    while True:

        sentence = connectionSocket.recv(1024).decode()
        if not sentence: break

        res = sentence.upper()

        if res == "QUIT": break

        print(f"    recved from: {addr}, {sentence} --> {res}")
        connectionSocket.send(res.encode())

    print('received: CLOSE')
    print('LISTENING')
    connectionSocket.close()
