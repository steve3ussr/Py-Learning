import multiprocessing as mp
import time


def f(interval, string):
    time.sleep(interval)
    print(f"{' '*8}{time.strftime('%M:%S')} --> {string}")


if __name__ == '__main__':
    print(f"START @ {time.strftime('%M:%S')}")
    p1 = mp.Process(target=f, args=(2, "it's proc_1"))
    p2 = mp.Process(target=f, args=(3, "it's proc_2"))

    p1.start()
    p1.join()
    p2.start()
