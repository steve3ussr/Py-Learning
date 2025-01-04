import asyncio

from websockets import ConnectionClosedError, ConnectionClosedOK
from websockets.asyncio.client import connect


async def hello():
    uri = "ws://127.0.0.1:8765"
    async with connect(uri) as websocket:
        try:
            while True:
                name = input("What's your message? ")

                await websocket.send(name)
                print(f">>> {name}")

                greeting = await websocket.recv()
                print(f"<<< {greeting}")

        except ConnectionClosedError:
            print(f"connection timeout. ")

        except ConnectionClosedOK:
            print(f"server closed. ")


if __name__ == "__main__":
    asyncio.run(hello())
