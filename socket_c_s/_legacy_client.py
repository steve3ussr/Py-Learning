# client
from socket import *

serverName = '127.0.0.1'
serverPort = 13000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:

    sentence = input("enter lowercase string: ")
    clientSocket.send(sentence.encode())

    if sentence == 'quit': break

    modifiedSentence = clientSocket.recv(1024)

    print(f"From server:            {modifiedSentence.decode()}")
clientSocket.close()
