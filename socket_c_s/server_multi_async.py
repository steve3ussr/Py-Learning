import asyncio


async def handler(reader, writer):
    try:
        while True:
            data = await reader.readline()
            message = data.decode()
            addr = writer.get_extra_info('peername')

            if not message or message.lower().strip() == 'quit':
                break

            message = message.upper()
            writer.write(message.encode())
            await writer.drain()

            # print(f"Received {message} from {addr}, Send: {message}")

    except ConnectionResetError:
        print('Connection RST, maybe cli closed. ')

    finally:
        print("Close the connection")

        if not writer.is_closing():
            writer.close()
            await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handler, '127.0.0.1', 13000, limit=65536*2)
    host, port = server.sockets[0].getsockname()
    print(f'Serving on {host} @ {port}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
