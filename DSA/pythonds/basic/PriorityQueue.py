from DSA.pythonds.trees.MaxBinaryHeap import MaxBinaryHeap
from DSA.pythonds.trees.MinBinaryHeap import MinBinaryHeap


class PriorityQueue(MaxBinaryHeap, MinBinaryHeap):
    def __init__(self, limit=None, *, mode='max'):

        if mode == 'max':
            if limit is None:
                super().__init__()
            else:
                super().__init__(limit)

            self.switchDown = super().switchDown
            self.enqueue = self.insert
            self.dequeue = self.delMax
            self.buildup = self.buildHeap

        elif mode == 'min':
            if limit is None:
                super(MaxBinaryHeap, self).__init__()
            else:
                super(MaxBinaryHeap, self).__init__(limit)

            self.switchDown = super(MaxBinaryHeap, self).switchDown
            self.enqueue = super(MaxBinaryHeap, self).insert
            self.dequeue = self.delMin
            self.buildup = super(MaxBinaryHeap, self).buildHeap
        else:
            raise TypeError('MODE ERROR')


if __name__ == '__main__':
    q = PriorityQueue(mode='min')

    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(5)
    q.enqueue(3)
    q.enqueue(1.5)
    print(q.heap)
    q.dequeue()
    # q.buildup([5, 9, 11, 14, 18, 19, 21, 33, 17, 27])
    print(q.heap)
    q.dequeue()
    print(q.heap)




