from client_mock import ClientMock
import asyncio
import random

_list_name = [f'cli-{chr(65 + i)}' for i in range(4)]
_list_interval = [[random.randint(1, 5) for _ in range(10)] for tmp in range(len(_list_name))]
_list_content = [[f"{chr(65 + j)}-{chr(104 + i) * 3}" for i in range(10)] for j in range(len(_list_name))]


async def cli_start(name, tasks):
    c = ClientMock(name, tasks)
    c.start()


async def main():
    cli_list = []
    for name, interval_list, content_list in zip(_list_name, _list_interval, _list_content):
        tasks = ((i, c) for i, c in zip(interval_list, content_list))
        cli_list.append(ClientMock(name, tasks))

    async with asyncio.TaskGroup() as tg:
        for cli in cli_list:
            tg.create_task(asyncio.to_thread(cli.start))


if __name__ == '__main__':
    asyncio.run(main())
