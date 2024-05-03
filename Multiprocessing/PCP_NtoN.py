from multiprocessing import Queue, Manager, Process, Value, Lock, RLock, Pool
import time
import random


def _producer(tup):
    l_print, q, item = tup
    q.put(item)
    with l_print:
        print(f"{time.strftime('%M:%S')}  --put->     {item}")
    time.sleep(2)


def producer(l_print, q, item_list):
    with Pool(processes=5) as pool:
        pool.map(_producer, [(l_print, q, item) for item in item_list])


def _consumer(tup):
    l_print, l_cnt, q, cnt, ma = tup

    while True:

        with l_cnt:
            if cnt.value >= ma.value:
                break
            item = q.get()
            cnt.value += 1

        with l_print:
            print(f"{time.strftime('%M:%S')}      <-get-- {item}, {cnt.value}/{ma.value}")

        time.sleep(3)


def consumer(l1, l2, q, cnt, ma):
    with Pool(processes=5) as pool:
        pool.map(_consumer, [(l1, l2, q, cnt, ma)] * 5)


if __name__ == '__main__':
    with Manager() as manager:
        q = manager.Queue(5)
        data = [_ * 10 for _ in range(10, 31)]
        cnt = manager.Value('i', 0)
        n = manager.Value('i', len(data))
        l_print = manager.Lock()
        l_cnt = manager.RLock()

        p_producer = Process(target=producer, args=(l_print, q, data))
        p_consumer = Process(target=consumer, args=(l_print, l_cnt, q, cnt, n))

        p_producer.start()
        p_consumer.start()

        p_producer.join()
        p_consumer.join()

        print('-----finished-----')
