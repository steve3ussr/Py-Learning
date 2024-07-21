class LinkedNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


class MyLinkedList:
    def __init__(self):
        self.cnt = 0
        self.head = LinkedNode()
        self.tail = LinkedNode()

        self.head.next = self.tail
        self.tail.prev = self.head

    def _debug(self):
        lst = []
        curr = self.head.next
        while curr != self.tail:
            lst.append(curr.val)
            curr = curr.next
        print(lst)

    def _index_validity(self, index):
        return 0 <= index < self.cnt

    def _index(self, index):
        curr = self.head.next

        for i in range(index):
            curr = curr.next
        return curr

    def _insert(self, index, val):
        back = self._index(index)
        front = back.prev
        new_node = LinkedNode(val=val, prev=front, next=back)

        front.next = new_node
        back.prev = new_node

        self.cnt += 1

    def _append(self, val):
        last = self.tail.prev
        new_node = LinkedNode(val=val, prev=last, next=self.tail)

        last.next = new_node
        self.tail.prev = new_node
        self.cnt += 1

    def _delete(self, index):
        target = self._index(index)
        front, back = target.prev, target.next

        front.next = back
        back.prev = front
        self.cnt -= 1

    def get(self, index):
        if self._index_validity(index):
            return self._index(index).val
        else:
            return -1

    def addAtHead(self, val):
        self._insert(0, val)

    def addAtTail(self, val):
        self._append(val)

    def addAtIndex(self, index, val):
        if index == self.cnt:
            self.addAtTail(val)
            return

        if not self._index_validity(index):
            return

        self._insert(index, val)

    def deleteAtIndex(self, index):
        if not self._index_validity(index):
            return

        self._delete(index)
