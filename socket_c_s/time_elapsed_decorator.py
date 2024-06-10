import time


def time_elapsed_print(func, *args, **kwargs):
    def inner():
        print(time.strftime('%X'))
        time_start = time.time()

        func(*args, **kwargs)

        print(time.strftime('%X'))
        time_end = time.time()

        print(f"{time_end - time_start}s elapsed.")
    return inner
