from multiprocessing import Queue, Manager, Process, Value, RLock
import time
import random


def producer(l, q, item_list):
    for item in item_list:
        q.put(item)
        with l:
            print(f"{time.strftime('%M:%S')}  --put->     {item}")
        time.sleep(2)


def consumer(l, q, ma):
    cnt = 0
    while cnt < ma.value:
        item = q.get()
        cnt += 1
        interval = random.random() * 3+1.5
        with l:
            print(f"{time.strftime('%M:%S')}      <-get-- {item}, {cnt}/{ma.value}")
        time.sleep(interval)


if __name__ == '__main__':
    q = Queue(5)
    data = [_ * 10 for _ in range(10, 31)]
    n = Value('i', len(data))
    l = RLock()

    p_producer = Process(target=producer, args=(l, q, data))
    p_consumer = Process(target=consumer, args=(l, q, n))

    p_producer.start()
    p_consumer.start()

    p_producer.join()
    p_consumer.join()

    print('-----finished-----')
