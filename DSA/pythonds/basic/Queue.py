class Queue(object):
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def dequeue(self):
        return self.items.pop()

    def enqueue(self, i):
        self.items.insert(0, i)

    def size(self):
        return len(self.items)

    def __str__(self):
        return f"{self.items}"

    __repr__ = __str__


if __name__ == '__main__':
    q = Queue()
    q.enqueue(1)
    q.enqueue(34265)
    q.dequeue()
    print(q)
