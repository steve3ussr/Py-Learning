import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError


async def hello(websocket):
    print(f"{websocket.remote_address} start. ")
    try:
        while True:
            rx = await websocket.recv()
            print(f"<<< {websocket.remote_address}: {rx}")

            tx = f"Server received {rx}!"

            await websocket.send(tx)
            print(f">>> {tx}")

    except ConnectionClosedOK:
        print(f"{websocket.remote_address} closed by client. ")

    except ConnectionClosedError:
        print(f"{websocket.remote_address} timeout. ")

    finally:
        print(f"connection with {websocket.remote_address} closed. ")
        await websocket.close()



async def main():
    async with serve(hello, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

    """
    # pseudo-code
    try:
        server = await serve(hello, "localhost", 8765)
    except [Exceptions]:
        pass
    finally:
        await server.close()
    """



if __name__ == "__main__":
    asyncio.run(main())
