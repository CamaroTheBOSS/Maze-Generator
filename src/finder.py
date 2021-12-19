from graph import *

def BreadthFirstSearch(F: Graph, startnode: int, goalnode: int):
    idx = startnode
    Visited = [idx]
    Backtracking = [idx]  # contains information about the solution
    journey = []
    while idx != goalnode:
        # 2.1 determining possible ways (to unvisited neighbours)
        ways = []
        for edge in F.edges:
            if edge[0] == idx or edge[1] == idx:
                if edge[0] in Visited and edge[1] in Visited:
                    pass
                else:
                    ways.append(edge)
        # 2.2 choose one randomly (if dead end facilitate backtracking)
        if len(ways) > 0:
            way = ways[0]
            ways.remove(way)
        else:  # dead end
            if len(Backtracking) > 1:
                idx = Backtracking[-2]
                del Backtracking[-1]
                continue
            else:
                break
        # 2.3 to Visited list add next node which way leads to and add this node to backtracking list
        if way[0] == idx:
            idx = way[1]
        else:
            idx = way[0]

        if way[0] == idx:
            Visited.append(way[0])
            Backtracking.append(way[0])
        else:
            Visited.append(way[1])
            Backtracking.append(way[1])
        # 2.4 track the journey of algorithm to have information about edges we must not delete
        journey.append(way)
    Solution = []
    for idx, element in enumerate(Backtracking):
        if idx != 0:
            Solution.append((Backtracking[idx - 1], Backtracking[idx]))

    return Solution
