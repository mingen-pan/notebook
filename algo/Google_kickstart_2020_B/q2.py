
def solution(routes, D):
    for route in routes[::-1]:
        k = D // route
        D = k * route
    return D

t = int(input())
for i in range(1, t + 1):
    n, D = [int(s) for s in input().split(" ")]
    arr = [int(s) for s in input().split(" ")]  # read a list of integers, 2 in this case
    ans = solution(arr, D)
    print("Case #{}: {}".format(i, ans))
