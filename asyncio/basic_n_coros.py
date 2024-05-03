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
    await asyncio.gather(* [func1(random.random()*20+5, f"task_{i + 1}") for i in range(10)] )


async def main_tg():
    async with asyncio.TaskGroup() as tg:
        for i in range(10):
            tg.create_task(func1(random.random()*20+5, f"task_{i + 1}"))


if __name__ == '__main__':
    # asyncio.run(main_gather())
    asyncio.run(main_tg())
