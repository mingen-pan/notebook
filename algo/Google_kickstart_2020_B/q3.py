

def solution(ins):
    stack = []
    cur = [0, 0]
    k = 1
    for ch in ins:
        if ch == "N":
            cur[1] -= 1
        elif ch == "S":
            cur[1] += 1
        elif ch == "E":
            cur[0] += 1
        elif ch == "W":
            cur[0] -= 1
        elif ch == "(":
            stack.append((cur[:], k))
            cur = [0, 0]
        elif ch == ")":
            prev, k = stack.pop()
            cur = [prev[0] + k * cur[0], prev[1] + k * cur[1]]
        else:
            k = int(ch)

    BASE = 1000000000
    return (cur[0] % BASE) + 1, (cur[1] % BASE) + 1



print(solution(""))

# print(solution("SSSEEE"))
# print(solution("N"))
# print(solution("N3(S)N2(E)N"))
# print(solution("2(3(NW)2(W2(EE)W))"))


t = int(input())
for i in range(1, t + 1):
    ans = solution(input())
    print("Case #{}: {} {}".format(i, ans[0], ans[1]))
