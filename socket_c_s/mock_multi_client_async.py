from client_mock import ClientMock
import asyncio
import random
from time_elapsed_decorator import time_elapsed_print


# global var setting
_list_name = [f'cli-id-{i}' for i in range(100)]
_list_interval = [[random.randint(1, 5) for _ in range(10)] for tmp in _list_name]
_list_message = [[f"cli-id-{j}-{(1000 + i)}" for i in range(10)] for j in range(len(_list_name))]

cli_list = []
for name, interval_list, content_list in zip(_list_name, _list_interval, _list_message):
    tasks = ((i, c) for i, c in zip(interval_list, content_list))
    cli_list.append(ClientMock(name, tasks))


async def _main():
    async with asyncio.TaskGroup() as tg:
        for cli in cli_list:
            print(f"start: {cli.name}")
            tg.create_task(asyncio.to_thread(cli.start))


@time_elapsed_print
def main():
    asyncio.run(_main())


if __name__ == '__main__':
    main()
