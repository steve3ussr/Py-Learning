import asyncio
import json
from websockets.asyncio.server import serve, ServerConnection, broadcast


USERS_SET = set()
CNT = 0

def update_user():
    data = json.dumps({'type': 'users', 'value': len(USERS_SET)})
    broadcast(USERS_SET, data)

def update_cnt():
    data = json.dumps({'type': 'cnt', 'value': CNT})
    broadcast(USERS_SET, data)


async def handler(conn: ServerConnection):
    global USERS_SET, CNT
    try:
        USERS_SET.add(conn)
        update_user()
        update_cnt()

        async for msg_raw in conn:
            msg = json.loads(msg_raw)
            if 'key' not in msg:
                continue

            if msg['key'] == 'minus':
                CNT -= 1
            elif msg['key'] == 'plus':
                CNT += 1
            else:
                continue
            update_cnt()

    finally:
        USERS_SET.remove(conn)
        update_user()


async def main():
    async with serve(handler, 'localhost', 6789) as server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())