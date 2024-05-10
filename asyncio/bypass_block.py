import asyncio
import time


def sleep_block(interval):
    time.sleep(interval)
    print(f"sleep_block end: {time.strftime('%X')}")


async def sleep_non_block(interval):
    await asyncio.sleep(interval)
    print(f"sleep_non_block: {time.strftime('%X')}")


async def main_block():
    _start = time.time()
    start = time.strftime('%X')
    print(f"start at {start}")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(sleep_non_block(6))
        sleep_block(3)
    _end = time.time()
    end = time.strftime('%X')
    print(f"start at {start}, {_end-_start}s elapsed. ")


async def main_non_block():
    _start = time.time()
    start = time.strftime('%X')
    print(f"start at {start}")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(sleep_non_block(6))
        tg.create_task(asyncio.to_thread(sleep_block, 3))
    _end = time.time()
    end = time.strftime('%X')
    print(f"start at {start}, {_end-_start:.1f}s elapsed. ")

if __name__ == '__main__':
    asyncio.run(main_non_block())
