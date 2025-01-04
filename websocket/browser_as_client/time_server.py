import websockets
import time
import asyncio
from websockets.asyncio.server import serve
from websockets.asyncio.server import ServerConnection


async def handler(conn: ServerConnection):
    try:
        while True:
            msg = time.strftime("%x-%X")
            await conn.send(msg)
            await asyncio.sleep(2)
    except websockets.exceptions.ConnectionClosedOK:
        pass


async def main():
    async with serve(handler, 'localhost', 6789) as server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
