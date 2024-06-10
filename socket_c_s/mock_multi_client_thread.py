from client_mock import ClientMock
import threading
from concurrent.futures import ThreadPoolExecutor
import random
from time_elapsed_decorator import time_elapsed_print
from multiprocessing.pool import ThreadPool

# global var setting
_list_name = [f'cli-id-{i}' for i in range(10000)]
_list_interval = [[1 for _ in range(10)] for tmp in _list_name]
_list_message = [[f"cli-id-{j}-{(1000 + i)}" for i in range(10)] for j in range(len(_list_name))]

cli_list = []
for name, interval_list, content_list in zip(_list_name, _list_interval, _list_message):
    tasks = ((i, c) for i, c in zip(interval_list, content_list))
    cli_list.append(ClientMock(name, tasks))


def kick_start(cli):
    print(f"{cli.name} start")
    cli.start()


@time_elapsed_print
def main_mp():
    with ThreadPool(processes=10000) as pool:
        pool.map(kick_start, cli_list)


@time_elapsed_print
def main_con():
    with ThreadPoolExecutor(max_workers=10000) as pool:
        pool.map(kick_start, cli_list)


if __name__ == '__main__':
    t_main = threading.Thread(target=main_con)
    t_main.start()
    t_main.join()
