import math


def solution(W, H, L, U, R, D):
    if L == 1 and U == 1:
        return 0.0
    if R == W and D == H:
        return 0.0
    if L == 1 and R == W:
        return 0.0
    if U == 1 and D == H:
        return 0.0

    pre_sum = [0, 0]
    for num in range(2, W + H + 1):
        pre_sum.append(pre_sum[-1] + math.log(num, 2))

    def prob(x, y):
        if x == 1 and y == 1:
            return 1
        n = x + y - 2
        r = min(x - 1, y - 1)
        log_numer = pre_sum[n] - pre_sum[n - r]
        # numer = reduce(op.mul, range(n, n - r, -1), 1)
        log_denom = pre_sum[r]
        return 2 ** (log_numer - log_denom - n)

    fail = 0
    if U != 1:
        for j in range(L, min(R, W - 1) + 1):
            fail += 0.5 * prob(U - 1, j)

        if R == W:
            for i in range(1, U):
                fail += 0.5 * prob(i, W - 1)

    if L != 1:
        for i in range(U, min(D, H - 1) + 1):
            fail += 0.5 * prob(i, L - 1)

        if D == H:
            for j in range(1, L):
                fail += 0.5 * prob(H - 1, j)

    return 1 - fail


def solution_dp(W, H, L, U, R, D):
    if L == 1 and U == 1:
        return 0.0
    if R == W and D == H:
        return 0.0
    if L == 1 and R == W:
        return 0.0
    if U == 1 and D == H:
        return 0.0

    def in_hole(x, y):
        return U <= x <= D and L <= y <= R

    dp = [[0] * (W + 1) for i in range(H + 1)]

    dp[1][1] = 1.0
    for i in range(2, H + 1):
        if in_hole(i, 1):
            dp[i][1] = 0
            break
        else:
            dp[i][1] = 0.5 * dp[i - 1][1]

    for j in range(2, W + 1):
        if in_hole(1, j):
            dp[1][j] = 0
            break
        else:
            dp[1][j] = 0.5 * dp[1][j - 1]

    for i in range(2, H + 1):
        for j in range(2, W + 1):
            if in_hole(i, j):
                continue
            if i == H:
                b = 1
            else:
                b = 0.5
            if j == W:
                a = 1
            else:
                a = 0.5
            dp[i][j] = a * dp[i - 1][j] + b * dp[i][j - 1]

    return dp[-1][-1]


print(solution(3, 3, 2, 2, 2, 2))
print(solution(5, 3, 1, 2, 4, 2))
print(solution(1, 10, 1, 3, 1, 5))
print(solution(6, 4, 1, 3, 3, 4))
print(solution(300, 300, 100, 2, 150, 300))
print(solution_dp(300, 300, 100, 2, 150, 300))

print(solution(10, 10, 5, 2, 5, 10))
print(solution_dp(10, 10, 5, 2, 5, 10))

print(solution(10, 10, 2, 8, 10, 8))
print(solution_dp(10, 10, 2, 8, 10, 8))

# t = int(input())
# for i in range(1, t + 1):
#     arr = [int(s) for s in input().split(" ")]
#     ans = solution(*arr)
#     print("Case #{}: {}".format(i, ans))
