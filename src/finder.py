from graph import *


# BreadthFirstSearch algorithm does not make us 100% sure that the found path is the shortest one
def BreadthFirstSearch(F: Graph, startnode: int, goalnode: int):
    # 1. Choosing random cell
    idx = startnode
    Visited = [idx]
    Backtracking = [idx]  # contains information about the solution

    # 2. While currentnode is not goalnode
    while idx != goalnode:
        # 2.1 determining possible ways (to unvisited neighbours)
        ways = []
        for e in F.edges[idx]:
            if e in Visited and idx in Visited:
                pass
            else:
                ways.append((idx, e))

        # 2.2 choose first way
        if len(ways) > 0:
            way = ways[0]
        else:  # dead end
            if len(Backtracking) > 0:
                idx = Backtracking[-2]
                del Backtracking[-1]
                continue
            else:
                break

        # 2.3 to Visited list add next node which way leads to and add this node to backtracking list
        idx = way[1]
        Visited.append(idx)
        Backtracking.append(idx)

    # 3. prepare Solution and return it
    Solution = {}
    # 3.1 Give structure of dictionary
    for i in range(len(F.edges)):
        Solution[i] = []

    # 3.1 Fill dictionary with connections
    for i in range(len(Backtracking)):
        if i > 0:
            Solution[Backtracking[i - 1]].append(Backtracking[i])
            Solution[Backtracking[i]].append(Backtracking[i - 1])
    return Solution
