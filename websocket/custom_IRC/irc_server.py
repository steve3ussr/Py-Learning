import asyncio
import time
import json
import logging
from collections import defaultdict, deque
from dataclasses import dataclass
from websockets.asyncio.server import broadcast, serve, ServerConnection


@dataclass(slots=True)
class UserInfo:
    name: str
    status: int = None
    last_active_time: float = None

@dataclass(slots=True)
class MsgInfo:
    ftime: str
    sender: str
    content: str


class DuplicateWindowError(BaseException):pass
class MaxUserError(BaseException): pass


USER_DICT = defaultdict(UserInfo)
USER_MAX = 5
USER_LIVE = set()
MSG_LIST = deque(maxlen=1000)
MSG_CACHE = deque(maxlen=10)


async def user_connect(conn: ServerConnection):
    user_ip, user_port = conn.remote_address

    """
    X in dict:
        X status=1     close window
        X status=0     activate
    X not in dict:
        X register     register and activate
        X max len      close window, raise
    """
    if user_ip in USER_DICT and USER_DICT[user_ip].status == 1:
        await conn.send(json.dumps({'type': 'alert_and_quit',
                                    'msg': "You can only open 1 window! "}))
        raise DuplicateWindowError

    if user_ip not in USER_DICT:
        if len(USER_DICT) >= USER_MAX:
            await conn.send(json.dumps({'type': 'alert_and_quit',
                                        'msg': "Max user number reached, cannot connect to IRC server. "}))
            raise MaxUserError
        else:
            await conn.send(json.dumps({'type': 'req_username'}))
            data = json.loads(await conn.recv())
            USER_DICT[user_ip] = UserInfo(name=data['username'])

    # activate
    user = USER_DICT[user_ip]
    user.status = 1
    user.last_active_time = time.time()
    USER_LIVE.add(conn)
    cnt = len(USER_LIVE)

    # sync msg
    for msg in MSG_CACHE:
        await conn.send(json.dumps({'type': 'user_broadcast',
                                    'msg': f"{msg.sender}: {msg.content}"}))

    await sys_broadcast(f"{user.name} joined in, "
                        f"{cnt} user{'s' if cnt>1 else ''} online. ")


async def user_disconnect(conn: ServerConnection):
    user = USER_DICT[conn.remote_address[0]]
    user.status = 0
    if conn in USER_LIVE:
        USER_LIVE.remove(conn)
    cnt = len(USER_LIVE)
    await sys_broadcast(f"{user.name} left, {cnt} user{'s' if cnt>1 else ''} online. ")


async def timer_save_msg():
    while True:
        await asyncio.sleep(60)
        with open(r"C:\tmp\irc_server_msg.log", 'a') as f:
            while MSG_LIST:
                msg = MSG_LIST.popleft()
                f.write(f"[{msg.ftime} {msg.sender}]: {msg.content}")



async def sys_broadcast(msg_raw: str):
    msg = json.dumps({'type': 'sys_broadcast',
                      'msg': "[System] " + msg_raw,
                      'cnt': len(USER_LIVE)})
    broadcast(USER_LIVE, msg)
    msg = MsgInfo(ftime=time.strftime("%X-%x"),
                            sender="SYSTEM",
                            content=msg_raw)
    MSG_LIST.append(msg)


async def user_broadcast(conn: ServerConnection, msg_raw: str):
    assert conn in USER_LIVE
    user_ip, user_port = conn.remote_address
    user = USER_DICT[user_ip]
    user.last_active_time = time.time()
    data = json.dumps({'type': 'user_broadcast',
                       'msg': f"{user.name}: " + msg_raw})
    broadcast(USER_LIVE, data)
    msg = MsgInfo(ftime=time.strftime("%X-%x"),
                            sender=user.name,
                            content=msg_raw)
    MSG_LIST.append(msg)
    MSG_CACHE.append(msg)


async def handler(conn: ServerConnection):
    try:
        await user_connect(conn)

        async for event_raw in conn:
            event = json.loads(event_raw)

            if event['type'] == 'send':
                msg = event['msg']
                await user_broadcast(conn, msg)

    except DuplicateWindowError:
        await conn.wait_closed()
    except MaxUserError:
        await conn.wait_closed()

    finally:
        if conn:
            await user_disconnect(conn)



async def main():
    async with serve(handler, "192.168.0.114", 6789) as server:
        asyncio.get_running_loop().create_task(timer_save_msg())
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
