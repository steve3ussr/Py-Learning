class Node(object):
    def __init__(self):
        self._data = None
        self._next = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, new_next):
        self._next = new_next


class Unorderlist(object):
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head is None

    def add(self, new_data):
        temp_node = Node()
        temp_node.data = new_data
        temp_node.next = self.head
        self.head = temp_node

    def length(self):
        cnt = 0
        temp = self.head
        while temp is not None:
            cnt += 1
            temp = temp.next
        return cnt

    def search(self, i):
        temp = self.head

        while temp is not None:
            if i == temp.data:
                return True
            temp = temp.next
        return False

    def remove(self, i):
        current = self.head
        last = None

        while current is not None:

            # 只要找到一样的就可以break
            if i == current.data:
                if last is None:
                    self.head = current.next
                else:
                    last.next = current.next
                break

            else:
                last = current
                current = current.next

    def append(self, new_data):
        current = self.head
        while current.next is not None:
            print(current.data)
            current = current.next
        temp_node = Node()
        temp_node.data = new_data
        current.next = temp_node

    def insert(self, new_data, target_index):
        if target_index == 0:
            self.add(new_data)
        elif target_index == self.length():
            self.append(new_data)
        elif target_index > self.length() or target_index < 0:
            raise IndexError('over the boundary')
        else:
            current = self.head
            last = None
            cnt = 0
            temp_node = Node()
            temp_node.data = new_data
            while cnt != target_index:
                cnt += 1
                last = current
                current = current.next
            last.next = temp_node
            temp_node.next = current

    def index(self, target_index):
        if target_index < self.length():
            temp = self.head
            cnt = 0
            while cnt != target_index:
                cnt += 1
                temp = temp.next
            return temp.data
        else:
            raise IndexError('over the boundary')

    def pop(self, *target_index):
        if target_index == ():
            target_index = self.length()-1

        if 0 <= target_index[0] <= self.length()-1:
            current = self.head
            last = None
            if target_index[0] == 0:
                target_data = current.data
                self.head = current.next
            else:
                cnt = 0
                while cnt != target_index[0]:
                    cnt += 1
                    last = current
                    current = current.next
                target_data = current.data
                last.next = current.next
        else:
            raise IndexError("over index boundary")

        return target_data

    def __str__(self):
        temp = self.head
        data_list = []
        while temp is not None:
            data_list.append(temp.data)
            temp = temp.next
        return f"{data_list}"

    def __repr__(self):
        print(self.__str__())

    def build(self, alist):
        for i in range(len(alist)-1, -1, -1):
            self.add(alist[i])
        return self


if __name__ == '__main__':
    mylist = Unorderlist()
    mylist.add(2)
    mylist.add(4)
    mylist.add(6)
    print(mylist)
    mylist.append(8)
    print(mylist)
    mylist.insert(10, 0)
    print(mylist)
    print('-----------------')
    mylist.remove(4)
    print(mylist)
    a = mylist.pop(2)
    print(a)
    print(mylist)
