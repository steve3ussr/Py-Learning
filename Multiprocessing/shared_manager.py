from multiprocessing import Process, Manager


def f(l):
    for i in range(len(l)):

        # Change here!
        if 1:
            l[i].value += 1 # not working

        else:
            tmp = l[i]      #
            tmp.value += 1  # works
            l[i] = tmp      #


class My:
    def __init__(self, a):
        self.value = a


if __name__ == '__main__':
    with Manager() as manager:
        l = manager.list([My(_*10) for _ in range(5)])

        p = Process(target=f, args=(l,))
        p.start()
        p.join()

        for i in range(len(l)):
            print(l[i].value)
