from functools import cache
from math import inf
from pprint import pprint


def rec_match_coin(coin_list, change):
    @cache
    def _rec(x):
        if x == 0:
            return 0, []

        ans = None

        for coin in coin_list:
            if coin > x:
                continue

            res = _rec(x - coin)
            if ans is None:
                ans = (res[0] + 1, res[1] + [coin])

            if res[0] + 1 < ans[0]:
                ans = (res[0] + 1, res[1] + [coin])

        return ans

    return _rec(change)


def dp2_match_coin(coin_list, change):
    dp = [[(inf, []) for j in range(change + 1)] for i in range(len(coin_list) + 1)]
    for x in range(len(coin_list)):
        dp[0][0] = (0, [])

    for x in range(1, len(coin_list) + 1):
        for y in range(change + 1):

            if 1 + dp[x][y - coin_list[x - 1]][0] < dp[x - 1][y][0]:
                dp[x][y] = (1 + dp[x][y - coin_list[x - 1]][0], dp[x][y - coin_list[x - 1]][1] + [coin_list[x - 1]])
            else:
                dp[x][y] = (dp[x - 1][y][0], dp[x - 1][y][1])

    return dp[-1][-1]


def dp1_match_coin(coin_list, change):
    dp = [(inf, []) for j in range(change + 1)]
    dp[0] = (0, [])

    for coin in coin_list:
        for y in range(1, change+1):
            if 1 + dp[y-coin][0] < dp[y][0]:
                dp[y] = (1 + dp[y-coin][0], dp[y-coin][1] + [coin])
            else:
                dp[y] = (dp[y][0], dp[y][1])

    return dp[-1]




if __name__ == '__main__':
    print(dp1_match_coin([25, 10, 1], 63))
