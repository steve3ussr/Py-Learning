import time
from multiprocessing import Process, Queue


def f_put(todo, item):
    todo.put(item)


def f_get(todo):
    print(todo.get())


if __name__ == '__main__':
    q = Queue()

    p1 = Process(target=f_put, args=(q, 'qwe'))
    p2 = Process(target=f_put, args=(q, 'asd'))
    p3 = Process(target=f_get, args=(q,))
    p1.start()
    p2.start()
    p3.start()

    print(f"{q.empty()}, {q.get()}, {q.empty()}")
