def hanoi(n, id_from, id_to, id_with, optional="半径为1的盘子"):
    if n == 1:
        print(f"将{optional} 从 {id_from} 移动到 {id_to}")
        return

    hanoi(n - 1, id_from, id_with, id_to)

    hanoi(1, id_from, id_to, id_with, f"半径为{n}的盘子")

    hanoi(n - 1, id_with, id_to, id_from)


if __name__ == '__main__':
    hanoi(5, 0, 1, 2)
