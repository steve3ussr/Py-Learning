from multiprocessing import Queue, Manager, Process, Value, Lock, RLock, Pool
import time
import random


def producer(l, q, item_list):
    for item in item_list:
        q.put(item)
        with l:
            print(f"{time.strftime('%M:%S')}  --put->     {item}")
        time.sleep(1)


def _consumer(tup):
    l, q, cnt, ma = tup
    while cnt.value < ma.value:
        item = q.get()
        with l:
            cnt.value += 1
            print(f"{time.strftime('%M:%S')}      <-get-- {item}, {cnt.value}/{ma.value}")
        time.sleep(7)


def consumer(l, q, cnt, ma):
    with Pool(processes=5) as pool:
        pool.map(_consumer, [(l, q, cnt, ma)] * 5)


if __name__ == '__main__':
    with Manager() as manager:
        q = manager.Queue(5)
        data = [_ * 10 for _ in range(10, 31)]
        cnt = manager.Value('i', 0)
        n = manager.Value('i', len(data))
        l = manager.RLock()

        p_producer = Process(target=producer, args=(l, q, data))
        p_consumer = Process(target=consumer, args=(l, q, cnt, n))

        p_producer.start()
        p_consumer.start()

        p_producer.join()
        p_consumer.join()

        print('-----finished-----')
