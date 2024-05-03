import os
import psutil


if __name__ == '__main__':
    pid = os.getpid()
    ppid = os.getppid()

    print(f"{ppid} --> {pid}")
    print(f"{ppid}: {psutil.Process(ppid).name()}")
    print(f"{pid}: {psutil.Process(pid).name()}")