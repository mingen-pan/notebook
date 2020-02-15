def solution(times, times_limit):
    # Your code here
    n = len(times)
    if n <= 2:
        return []

    def find_shortest_path(times):
        # edges records the shortest distance from i to j
        edges = [times[i][:] for i in range(n)]
        # v_included records the nodes covered by the shortest path from i to j
        v_included = [[{i, j} for j in range(n)] for i in range(n)]

        # Floyd Algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if edges[i][k] + edges[k][j] < edges[i][j]:
                        edges[i][j] = edges[i][k] + edges[k][j]
                        v_included[i][j] = v_included[i][k].union(v_included[k][j])
        return edges, v_included

    edges, v_included = find_shortest_path(times)

    # negative cycle means every bunny can be rescued
    for i in range(n):
        if edges[i][i] < 0:
            return list(range(n - 2))

    visited = [0] * n
    ans = [tuple()]

    def to_ans(visited):
        """
        convert the number-based visited array to the index-based array
        e.g. [0, 1, 0, 0] => [0]
        """
        ans = []
        for i in range(n - 2):
            if visited[i + 1]:
                ans.append(i)
        return tuple(ans)

    def dfs(i, time_limit):
        if i == n - 1:
            if time_limit >= 0:
                new_ans = to_ans(visited)
                if len(new_ans) > len(ans[0]):
                    ans[0] = new_ans
                    return
                elif len(new_ans) == len(ans[0]):
                    ans[0] = min(ans[0], new_ans)
            return

        def visit(i, j):
            for k in v_included[i][j]:
                visited[k] += 1
            dfs(j, time_limit - edges[i][j])
            for k in v_included[i][j]:
                visited[k] -= 1

        for j in range(1, n - 1):
            if visited[j] == 0:
                visit(i, j)
        visit(i, n - 1)

    dfs(0, times_limit)
    return list(ans[0])


