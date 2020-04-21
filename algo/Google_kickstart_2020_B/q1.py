

def solution(heights):
    if len(heights) <= 2:
        return 0
    count = 0
    for i in range(1, len(heights) - 1):
        if heights[i] > heights[i-1] and heights[i] > heights[i+1]:
            count += 1
    return count


t = int(input())
for i in range(1, t + 1):
    input()
    arr = [int(s) for s in input().split(" ")]  # read a list of integers, 2 in this case
    ans = solution(arr)
    print("Case #{}: {}".format(i, ans))
