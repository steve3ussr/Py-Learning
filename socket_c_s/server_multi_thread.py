from socket import *
import threading


def handler(cli_sock, addr):
    print('entered')
    try:
        while True:
            message = cli_sock.recv(1024).decode()
            if not message or message.lower().strip() == 'quit':
                break

            res = message.lower()
            cli_sock.send(res.encode())
            # print(f"server recv: {addr}, {message} --> {res}")

    except ConnectionResetError:
        print('Connection RST, maybe cli closed. ')

    finally:
        cli_sock.close()
        print(f"{addr} closed, LISTENING NOW.")


def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 13000))
    server_socket.listen(1)
    print(f'Serving on 127.0.0.1:13000')

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handler, args=(client_socket, addr))
        client_thread.start()


if __name__ == "__main__":
    main()


