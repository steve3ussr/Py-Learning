import time
import websockets
import asyncio
from websockets.asyncio.server import serve, broadcast, ServerConnection


conn_set = set()

async def register(conn: ServerConnection):
    conn_set.add(conn)
    print(len(conn_set))
    try:
        await conn.wait_closed()
    finally:
        conn_set.remove(conn)

async def send_time():
    while True:
        msg = time.strftime('%x-%X')
        broadcast(conn_set, msg)
        await asyncio.sleep(2)

async def main():
    async with serve(register, 'localhost', 6789) as server:
        await send_time()



if __name__ == '__main__':
    asyncio.run(main())
