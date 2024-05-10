import asyncio
import time
import random


async def func1(interval, string):
    begin = time.time()
    begin_str = time.strftime('%X')
    await asyncio.sleep(interval)
    end = time.time()
    end_str = time.strftime('%X')
    print(f"{begin_str} -> {end_str}, {end - begin:>5.2f}s: {string}")


async def main_gather():
    task_set = set()
    for i in range(10):
        coro = func1(random.random()*5+3, f"task_{i + 1}")
        task = asyncio.create_task(coro)
        task_set.add(task)
    await asyncio.gather(* task_set )


async def main_tg():
    async with asyncio.TaskGroup() as tg:
        task_set = set()
        for i in range(10):
            coro = func1(random.random()*5+3, f"task_{i + 1}")
            task = tg.create_task(coro)
            task_set.add(task)


if __name__ == '__main__':
    # asyncio.run(main_gather())
    asyncio.run(main_tg())
