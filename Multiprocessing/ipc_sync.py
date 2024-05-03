import multiprocessing as mp

def inc_lock(l, shared):
    with l:
        for _ in range(1000):
            shared.value += 1


def inc(shared):
    for _ in range(1000):
        shared.value += 1


if __name__ == "__main__":
    # 创建共享变量和锁
    a = mp.Value('i', 0)
    lock = mp.Lock()

    # 1-lock, 0-unsafe
    if 1:
        processes = [mp.Process(target=inc_lock, args=(lock, a)) for _ in range(10)]
    else:
        processes = [mp.Process(target=inc, args=(a, )) for _ in range(10)]

    # 启动进程
    for p in processes:
        p.start()

    # 等待进程结束
    for p in processes:
        p.join()

    print("Final value:", a.value)