import random as rd
from shapes import *
from intersect import *
from finder import *


# Author: Kacper Plesiak
# It is worth to read README.md file at https://github.com/CamaroTheBOSS/Maze-Generator

# Constructing grid of cells (blue graph) with given shape (not implemented yet) and size
def prepareGraph(G: Graph, columns: int = 5, rows: int = 5, shape='Hexagon'):  # a - edgeSize
    a = 5
    # 1. Preparing shapes:
    if shape == 'Hexagon':
        for c in range(columns):
            for r in range(rows):
                Hex(G, c, r, a)
    elif shape == 'Triangle':
        for c in range(columns):
            for r in range(rows):
                Triangle(G, c, r, a)
    elif shape == 'Square':
        for c in range(columns):
            for r in range(rows):
                Square(G, c, r, a)


# Creating graph F which is dual to G, grid of possible ways (red graph)
def DualGraph(G: Graph):
    F = Graph()
    a = 5
    # 1. Defining nodes, by computing center of each face
    for face in G.faces:
        x = 0
        y = 0

        for node in face:
            x += G.nodes[node][0]
            y += G.nodes[node][1]
        x /= len(face)
        y /= len(face)
        F.addNode(x, y)

    # 2. Defining edges with k-nearest neighbours algorithm (here the condition value is choosen)
    neighnum = len(G.faces[0])
    if neighnum == 6:
        condition = 3 * a
    elif neighnum == 3:
        condition = 0.95 * a
    elif neighnum == 4:
        condition = 1.1 * a

    # 2.1 k-nearest-neighbours algorithm
    for key, node in F.nodes.items():

        k = []  # nearest nodes indexes
        for kn, n in F.nodes.items():
            if n == node:
                continue
            d = abs(node[0] - n[0]) + abs(node[1] - n[1])
            if d < condition:  # if distance of node is smaller than max allowable distance (condition), add node to nearest
                k.append(kn)
                if len(k) == neighnum:
                    break

        for idx in k:
            F.addEdge(key, idx)

    return F


# creating the actual maze, forming possible moving ways in planar graph with randomized depth-breadth search algorithm
def Maze(F: Graph):
    # 1. Choosing random cell
    idx = rd.randint(0, len(F.nodes) - 1)
    Visited = [idx]
    Backtracking = [idx]
    journey = []  # ways traveled by the algorithm

    # 2. While any node is unvisited
    while len(Visited) != len(F.nodes):
        # 2.1 determining possible ways (to unvisited neighbours)
        ways = []
        for e in F.edges[idx]:
            if e in Visited and idx in Visited:
                pass
            else:
                ways.append((idx, e))

        # 2.2 choose one randomly (if dead end backtrack)
        if len(ways) > 0:
            rdn = rd.randint(0, len(ways) - 1)
            way = ways[rdn]
        else:  # dead end
            if len(Backtracking) > 0:
                idx = Backtracking[-1]
                del Backtracking[-1]
                continue
            else:
                break

        # 2.3 to Visited list add next node which way leads to and add this node to backtracking list
        idx = way[1]
        Visited.append(idx)
        Backtracking.append(idx)

        # 2.4 Add way to journey
        journey.append(way)

    # 3. Delete unused edges
    for key, neighbours in F.edges.items():

        # 3.1 Find connections to delete
        ToRemove = []
        for node in neighbours:
            if (key, node) not in journey and (node, key) not in journey:
                ToRemove.append(node)

        # 3.2 Delete found connections
        for element in ToRemove:
            F.edges[key].remove(element)
            F.edges[element].remove(key)


# deleting walls (blue edges) if wall intersects with ways (red edges)
def DeleteIntersections(G: Graph, F: Graph):

    # For each way find wall which intersect this specific way and delete this specific wall
    for index, face in enumerate(G.faces):  # face index is equal to node index assigned to this face
        Blackedges = {}
        Bluedges = {}
        Blackedges[index] = F.edges[index]
        for n in range(len(face)):
            Bluedges[face[n - 1]] = [face[n]]

        for Fkey, Fneighbours in Blackedges.items():
            for Fn in Fneighbours:
                f1 = F.nodes[Fkey]
                f2 = F.nodes[Fn]

                for Gkey, Gneighbours in Bluedges.items():
                    for Gn in Gneighbours:
                        g1 = G.nodes[Gkey]
                        g2 = G.nodes[Gn]
                        if doIntersect(f1, f2, g1, g2):
                            if Gn in G.edges[Gkey]:
                                G.edges[Gkey].remove(Gn)
                                G.edges[Gn].remove(Gkey)
                            break


# Algorithm:
Z = Graph()
# 1.
cols = 40
rows = 40
prepareGraph(Z, columns=cols, rows=rows, shape='Hexagon')
# 2.
Zd = DualGraph(Z)
# 3.
Maze(Zd)
# 4.
DeleteIntersections(Z, Zd)

# Search Algorithm BFS from node 0 to node 60*40 - 1 (last one)
S = Graph()
S.nodes = Zd.nodes.copy()
S.edges = BreadthFirstSearch(Zd, 0, cols*rows-1)

# Plotting
Z.plotGraph()  # blue grid
#Zd.plotGraph(color='k')  # black ways
S.plotGraph(color='r')  # red ways

plt.show()
