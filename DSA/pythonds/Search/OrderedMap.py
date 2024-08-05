class OrderedMap:
    def __init__(self, init_size=10, utilization=0.7):
        self.minsize = init_size
        self.maxsize = init_size
        self.size = 0
        self.utilization = max(0.1, min(utilization, 1))

        self.indices: list = [None for i in range(self.maxsize)]
        self.entries = []
        self.access = []

    def put(self, key, value):
        hash_raw = hash(key)
        hash_masked = hash_raw & (self.maxsize - 1)
        offset = 0

        while True:
            hash_masked = (hash_masked + offset ** 2) % self.maxsize
            index = self.indices[hash_masked]

            if index is None:
                self.indices[hash_masked] = len(self.entries)
                self.entries.append((hash_raw, key, value))
                self.access.append(True)
                self.size += 1
                self.dyna()
                break

            if self.access[index] and self.entries[index][1] == key:
                self.entries[index] = (hash_raw, key, value)
                break

            offset += 1

    def get(self, key):
        hash_raw = hash(key)
        hash_masked = hash_raw & (self.maxsize - 1)
        offset = 0

        while True:
            hash_masked = (hash_masked + offset ** 2) % self.maxsize
            index = self.indices[hash_masked]

            if index is None:
                raise KeyError
            if self.entries[index][1] == key and self.access[index]:
                return index

            offset += 1

    def dyna(self):
        if self.size >= self.utilization * self.maxsize:
            self.maxsize *= 2
        elif self.minsize < self.size <= self.maxsize // 4:
            self.maxsize = max(self.minsize, self.maxsize // 2)
        else:
            return

        self.indices: list = [None for i in range(self.maxsize)]
        cnt = 0
        lst_gc = []

        for i, (accessible, (hash_raw, key, value)) in enumerate(zip(self.access, self.entries)):
            if not accessible:
                lst_gc.append(i)
                continue

            hash_masked = hash_raw & (self.maxsize - 1)
            offset = 0

            while True:
                hash_masked = (hash_masked + offset ** 2) % self.maxsize
                index = self.indices[hash_masked]

                if index is None:
                    self.indices[hash_masked] = cnt
                    cnt += 1
                    break

                offset += 1

        self.size = cnt

        for i in lst_gc[::-1]:
            self.access.pop(i)
            self.entries.pop(i)

    def delete(self, key):
        index = self.get(key)
        self.access[index] = False
        self.size -= 1
        self.dyna()

    def __str__(self):
        lst = []
        for accessible, (hash_raw, key, value) in zip(self.access, self.entries):
            if accessible:
                lst.append(f"{key:<4}: {value}")

        res = ", \n".join(lst)
        res += "\n---- SEGMENT ----\n"
        res += f"size: {self.size}, {len(lst)}\n"
        res += f"maxsize: {self.maxsize}\n"
        res += "---- THE END ----"
        return res

    __repr__ = __str__

    def __contains__(self, key):
        try:
            self.get(key)
        except KeyError:
            return False
        return True

    def __setitem__(self, key, value):
        self.put(key, value)

    def __getitem__(self, key):
        index = self.get(key)
        return self.entries[index][2]


if __name__ == '__main__':
    dct = OrderedMap()

    for i in range(50):
        char = chr(i + 97)
        dct.put(char, i + 1)

    dct.delete('a')

    for i in range(1, 35):
        char = chr(i + 97)
        dct.delete(char)

    for i in range(20):
        char = chr(i + 97)
        dct.put(char, i + 1)

    for i in range(20):
        char = chr(i + 97)
        print(f"{char} -> {dct[char]}")

