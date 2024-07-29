class SearchUtils:
    def __init__(self):
        pass

    @classmethod
    def disordered_search(cls, lst, target):
        for i, v in enumerate(lst):
            if v == target:
                return i
        return None

    @classmethod
    def ordered_search(cls, lst, target):
        for i, v in enumerate(lst):
            if v == target:
                return i
            elif v > target:
                return None
        return None

    @classmethod
    def binary_search(cls, lst, target):

        lo, hi = 0, len(lst)-1
        # 假设:
        # lo的左侧(不包含lo)都 < target
        # hi的右侧(不包含hi)都 > target

        while lo <= hi:
            mid = (lo + hi) // 2

            if lst[mid] > target:
                hi = mid - 1
            elif lst[mid] < target:
                lo = mid + 1
            elif lst[mid] == target:
                return mid

        if hi == -1:
            print("target < min[list]")
        elif lo == len(lst):
            print("target > max[list]")
        else:
            print(f"None match, the closest answer is: {lst[hi]} < [{target}] < {lst[lo]}")
        return None


if __name__ == '__main__':
    seq = [17, 20, 26, 31, 44, 54, 55, 65, 77, 93]
    x = 53
    print(SearchUtils.disordered_search(seq, x))
    print(SearchUtils.ordered_search(seq, x))
    print(SearchUtils.binary_search(seq, x))
