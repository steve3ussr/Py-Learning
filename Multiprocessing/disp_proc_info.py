import multiprocessing as mp
import time
import os
import platform


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

    if platform.system() == 'Linux':
        print('-------------------------')
        os.system("pstree")
        print('-------------------------')
    elif platform.system() == 'Windows':
        print('-------------------------')
    else:
        pass


def f(name):
    info('function f')
    print('hello', name)


if __name__ == '__main__':
    info('main line')
    p1 = mp.Process(target=f, args=('bob',))
    p2 = mp.Process(target=f, args=('dick',))
    p1.start()
    p1.join()
    p2.start()
    p2.join()
