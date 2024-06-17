import threading
import time


class RecycleTimer(threading.Timer):
    def run(self):
        while not self.finished.is_set():
            time.sleep(self.interval)
            self.function(*self.args, **self.kwargs)
        self.finished.set()


def func(descr):
    print(descr)


if __name__ == '__main__':
    t1 = RecycleTimer(3, function=func, args=("t1", ))
    t2 = RecycleTimer(1, function=func, args=("t2",))
    t1.start()
    t2.start()
