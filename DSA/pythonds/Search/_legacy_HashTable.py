class HashTable(object):
    def __init__(self):
        self.size = 11
        self.slot = [None] * self.size
        self.data = [None] * self.size

    @staticmethod
    def hash_func(key, a_int):
        return key % a_int

    @staticmethod
    def rehash_func(old_hash, a_int):
        return (old_hash + 1) % a_int

    def put(self, k, v):
        hash_val = self.hash_func(k, len(self.slot))

        if self.slot[hash_val] is None:
            self.slot[hash_val] = k
            self.data[hash_val] = v
        elif self.slot[hash_val] == k:
            self.data[hash_val] = v
        else:
            flg = 1
            while flg:
                rehash_val = self.rehash_func(hash_val, len(self.slot))
                if self.slot[rehash_val] is None:
                    flg = 0
                    self.slot[rehash_val] = k
                    self.data[rehash_val] = v
                elif self.slot[rehash_val] == k:
                    flg = 0
                    self.data[rehash_val] = v
                else:
                    hash_val = rehash_val

    def get(self, k):
        """
        return self.data[index]
        """
        index = self._get(k)
        if index is not None:
            return self.data[index]
        else:
            return None

    def _get(self, k):
        """
        return index
        """
        init_slot = self.hash_func(k, len(self.slot))
        if self.slot[init_slot] == k:
            return init_slot
        else:

            rehash_slot = self.rehash_func(init_slot, len(self.slot))
            while rehash_slot != init_slot:
                if self.slot[rehash_slot] == k:
                    return rehash_slot
                else:
                    rehash_slot = self.rehash_func(rehash_slot, len(self.slot))
            return None

    def del_map(self, k):
        if index := self._get(k) is not None:
            self.slot[index] = None
            self.data[index] = None
        else:
            pass

    def len(self):
        pass

    def __contains__(self, item):
        return True if self.get(item) is not None else False

    def __setitem__(self, key, value):
        self.put(key, value)

    def __getitem__(self, k):
        return self.get(k)


if __name__ == '__main__':
    h = HashTable()
    h[54] = 'cat'
    h[26] = 'dog'
    h[93] = 'lion'
    h[17] = 'tiger'
    h[77] = 'bird'
    h[31] = 'cow'
    h[44] = 'goat'
    h[55] = 'pig'
    h[20] = 'chicken'

    print(h.slot)
    print(h.data)

    print(h[20])
    print(h[17])
    h[20] = 'zsa'
    print(h.slot)
    print(h.data)
    print(h[100])

    print(1 in h)
    print(17 in h)
