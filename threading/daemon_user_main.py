import threading
import time


def worker_user(descr, interval, lock):
    with lock:
        print(f"{time.strftime('%X')}: user thread {descr} - start.")

    time.sleep(interval)

    with lock:
        print(f"{time.strftime('%X')}: user thread {descr} - start.")


def worker_daemon(descr, interval, lock):
    while True:
        time.sleep(interval)
        with lock:
            print(f"{time.strftime('%X')}: Daemon {descr} - working...")


if __name__ == '__main__':
    print(f"{time.strftime('%X')}: MaiNThread - started. ")
    l = threading.Lock()
    t_user = threading.Thread(target=worker_user, args=('USER', 10, l))
    t_user.start()
    t_daemon = threading.Thread(target=worker_daemon, args=('DAEMON', 1, l))
    t_daemon.daemon = True
    t_daemon.start()

    time.sleep(5)
    print(f"{time.strftime('%X')}: MaiNThread - end. ")
