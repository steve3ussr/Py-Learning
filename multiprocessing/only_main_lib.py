import multiprocessing as mp
import psutil
import os

class MyProc(mp.Process):
    def run(self):
        print('this is my proc')


def foo():
    print(f"{psutil.Process(os.getpid()).name()} - {__name__}")
    p = MyProc()
    p.start()
