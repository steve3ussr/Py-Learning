import asyncio
import time
import random
from pprint import pprint


async def func1(interval, string):
    begin = time.time()
    begin_str = time.strftime('%X')
    await asyncio.sleep(interval)
    end = time.time()
    end_str = time.strftime('%X')
    return f"{begin_str} -> {end_str}, {end - begin:>5.2f}s: {string}"


async def main_gather():
    task_set = []
    for i in range(10):
        coro = func1(random.random() * 5 + 3, f"task_{i + 1}")
        task = asyncio.create_task(coro)
        task_set.append(task)
    await asyncio.gather(*task_set)

    return [task.result() for task in task_set]


async def main_tg():
    async with asyncio.TaskGroup() as tg:
        task_set = []
        for i in range(10):
            coro = func1(random.random() * 5 + 3, f"task_{i + 1}")
            task = tg.create_task(coro)
            task_set.append(task)

    return [task.result() for task in task_set]


if __name__ == '__main__':
    res = asyncio.run(main_gather())
    # res = asyncio.run(main_tg())

    pprint(res)
