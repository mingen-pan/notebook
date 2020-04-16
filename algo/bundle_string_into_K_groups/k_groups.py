from collections import defaultdict
from heapq import heapify, heappop, heappush

"""
Question:

Pip has N strings. Each string consists only of letters from A to Z. Pip would like to bundle their strings into groups 
of size K. Each string must belong to exactly one group.

The score of a group is equal to the length of the longest prefix shared by all the strings in that group. For example:

The group {RAINBOW, RANK, RANDOM, RANK} has a score of 2 (the longest prefix is 'RA').

The group {FIRE, FIREBALL, FIREFIGHTER} has a score of 4 (the longest prefix is 'FIRE').

The group {ALLOCATION, PLATE, WORKOUT, BUNDLING} has a score of 0 (the longest prefix is '').

Please help Pip bundle their strings into K groups, such that the sum of scores of the groups is maximized.
"""


class Node:
    def __init__(self, depth, parent):
        self.depth = depth
        self.parent = parent
        self.children = set()

    def __lt__(self, other):
        return self.depth < other.depth


def make_trie():
    return defaultdict(make_trie)


def solution(strs, K):
    trie = make_trie()
    for s in strs:
        node = trie
        for ch in s:
            node = node[ch]
        if True not in node:
            node[True] = 1
        else:
            node[True] += 1

    # depth parent children
    node_tree = Node(0, None)
    leaves = set()
    total = [0]

    def dfs(node, parent, depth):
        if True in node or len(node) > 1:
            cur = Node(depth, parent)
            parent.children.add(cur)

            # this is the leaf
            if len(node) == 0 and node[True] == 1:
                leaves.add(cur)
                total[0] += depth
                return

            # make some fake leaves
            if True in node:
                for i in range(node[True]):
                    leaf = Node(depth, cur)
                    cur.children.add(leaf)
                    leaves.add(leaf)
                total[0] += depth * node[True]

            for child in node.values():
                if isinstance(child, int):
                    continue
                dfs(child, cur, depth + 1)
        else:
            for child in node.values():
                dfs(child, parent, depth + 1)

    for child in trie.values():
        dfs(child, node_tree, 1)

    # get two leaves of a node, whose depth is smallest.
    def get_two_leaves(node):
        # filter the leaves
        leaves = [child for child in node.children if \
                  len(child.children) == 0]
        if len(leaves) < 2:
            return None, None
        heapify(leaves)
        a = heappop(leaves)
        b = heappop(leaves)
        return a, b

    # the score of merge two nodes = sum(child.depth) - parent.depth
    # push the node into a heap based on its the difference in depth
    def push_node(pq, node):
        a, b = get_two_leaves(node)
        if a is None:
            return
        diff = a.depth + b.depth - node.depth
        heappush(pq, (diff, node, a, b))

    # find out all the parent nodes of leaves
    next_nodes = set()
    for leaf in leaves:
        next_nodes.add(leaf.parent)

    pq = []
    for node in next_nodes:
        push_node(pq, node)

    while len(leaves) > K:
        diff, node, a, b = heappop(pq)
        total[0] -= diff
        leaves.remove(a)
        leaves.remove(b)
        node.children.remove(a)
        node.children.remove(b)
        if len(node.children) == 0:
            leaves.add(node)
            push_node(pq, node.parent)
        else:
            child = Node(node.depth, node)
            node.children.add(child)
            leaves.add(child)
            push_node(pq, node)

    return total[0]


strs = ["G", "G", "GO", "GO", "GOO", "GOO", "GOOO", "GOOO"]
K = 2

print(solution(strs, K))
