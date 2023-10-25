class ListNode:
    def __init__(self, data=None, node=None):
        self.data = data
        self.next = node


class LinkedList:
    def __init__(self, iterable_obj):
        self.dumb = ListNode(None, None)
        self.len = len(iterable_obj)
        self.__build_list(iterable_obj)

    def __build_list(self, lst):
        tmp = self.dumb
        for obj in lst:
            tmp.next = ListNode(obj, None)
            tmp = tmp.next

    def __str__(self):
        res = []
        tmp = self.dumb
        while tmp.next:
            res.append(tmp.next.data)
            tmp = tmp.next
        return " -> ".join(map(str, res))


if __name__ == '__main__':
    linked_list = LinkedList(range(10))
    print(linked_list)
    enumerate
