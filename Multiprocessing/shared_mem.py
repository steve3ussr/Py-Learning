import multiprocessing as mp


def f_lock(l, n, a):
    with l:
        n.value += 1
        for i in range(len(a)):
            a[i] += 1

def f(n, a):
    for _ in range(100):
        n.value += 1
        for i in range(len(a)):
            a[i] += 1
        n.value -= 1
        for i in range(len(a)):
            a[i] -= 1


if __name__ == '__main__':
    num = mp.Value('i', 0)
    arr = mp.Array('i', range(5))
    lock = mp.Lock()

    procs = [mp.Process(target=f, args=(num, arr)) for _ in range(10)]

    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print(num.value)
    print(arr[:])
