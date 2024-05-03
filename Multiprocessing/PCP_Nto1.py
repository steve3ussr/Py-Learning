from multiprocessing import Queue, Manager, Process, Value, Lock, RLock, Pool
import time
import random


def _producer(tup):
    l, q, item = tup
    q.put(item)
    with l:
        print(f"{time.strftime('%M:%S')}  --put->     {item}")
    time.sleep(2)


def producer(l, q, item_list):

    with Pool(processes=5) as pool:
        pool.map(_producer, [(l, q, item) for item in item_list])


def consumer(l, q, ma):
    cnt = 0
    while cnt < ma.value:
        item = q.get()
        cnt += 1
        interval = random.random() * 3 + 1.5
        with l:
            print(f"{time.strftime('%M:%S')}      <-get-- {item}, {cnt}/{ma.value}")
        time.sleep(interval)


if __name__ == '__main__':
    with Manager() as manager:
        q = manager.Queue(5)
        data = [_ * 10 for _ in range(10, 31)]
        n = Value('i', len(data))
        l = manager.RLock()

        p_producer = Process(target=producer, args=(l, q, data))
        p_consumer = Process(target=consumer, args=(l, q, n))

        p_producer.start()
        p_consumer.start()

        p_producer.join()
        p_consumer.join()

        print('-----finished-----')
