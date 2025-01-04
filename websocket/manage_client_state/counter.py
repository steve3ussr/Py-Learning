import asyncio
import json
import logging
from websockets.asyncio.server import broadcast, serve, ServerConnection


logging.basicConfig()
USERS = set()
VALUE = 0

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def value_event():
    return json.dumps({"type": "cnt", "value": VALUE})

async def counter(conn: ServerConnection):
    global USERS, VALUE
    try:
        # Register user
        USERS.add(conn)
        broadcast(USERS, users_event())
        # Send current state to user
        await conn.send(value_event())
        # Manage state changes
        async for message in conn:
            event = json.loads(message)
            print(event)
            if event["key"] == "minus":
                VALUE -= 1
                broadcast(USERS, value_event())
            elif event["key"] == "plus":
                VALUE += 1
                broadcast(USERS, value_event())
            else:
                logging.error("unsupported event: %s", event)
    finally:
        # Unregister user
        USERS.remove(conn)
        broadcast(USERS, users_event())

async def main():
    async with serve(counter, "localhost", 6789):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())