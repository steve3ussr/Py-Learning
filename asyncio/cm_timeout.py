import asyncio
import time


async def coro(interval):
    await asyncio.sleep(interval)
    print('coro finished')


async def main():
    try:
        async with asyncio.timeout(10) as cm:
            t = asyncio.get_event_loop().time()
            # cm.reschedule(t+10)
            await coro(6)
            await coro(6)
            await coro(6)

    except TimeoutError:
        print('coro timeout')




if __name__ == '__main__':
    asyncio.run(main())
