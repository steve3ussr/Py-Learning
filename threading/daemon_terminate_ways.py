import threading
import time


def daemon_abrupt(descr, lock: threading.Lock):
    with lock:
        print(f"daemon-{descr} started.")

    while True:
        time.sleep(1)
        with lock:
            print(f"daemon-{descr} is still working.")

    with lock:
        print(f"daemon-{descr} terminated.")


def daemon_graceful(descr, lock: threading.Lock, event: threading.Event):
    with lock:
        print(f"daemon-{descr} started.")

    while not event.is_set():
        time.sleep(1)
        with lock:
            print(f"daemon-{descr} is still working.")

    with lock:
        print(f"daemon-{descr} terminated.")


if __name__ == '__main__':
    event_stop = threading.Event()
    lock_print = threading.Lock()

    threads_abrupt = []
    for i in range(3):
        t = threading.Thread(target=daemon_abrupt, args=(f"id-{i}", lock_print))
        t.daemon = True
        threads_abrupt.append(t)

    threads_graceful = []
    for i in range(3):
        t = threading.Thread(target=daemon_graceful, args=(f"id-{i}", lock_print, event_stop))
        threads_graceful.append(t)

    mode_options = ('abrupt', 'graceful')
    mode = mode_options[0]  # ------------- MAIN SWITCH -------------

    if mode == 'abrupt':
        for t in threads_abrupt:
            t.start()
        time.sleep(5)  # simulate main thread works

    elif mode == 'graceful':
        for t in threads_graceful:
            t.start()
        time.sleep(5)  # simulate main thread works
        event_stop.set()

    print("MainThread exit. ")
