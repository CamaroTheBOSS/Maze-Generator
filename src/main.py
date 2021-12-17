import numpy as np
import random as rd
import matplotlib.pyplot as plt
from shapes import *
from intersect import *


# Author: Kacper Plesiak
# it is worth to read README.md file at https://github.com/CamaroTheBOSS/Maze-Generator
# if you like my project please star it at github :D

# returns subtraction of two lists [1, 2, 3, 4] - [1, 4] = [2, 3]
def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


# constructing grid of cells (blue graph) with given shape (not implemented yet) and size
def prepareGraph(G: Graph, columns: int = 5, rows: int = 5):  # a - edgeSize
    a = 5
    # 1. preparing Hexes
    for c in range(columns):
        for r in range(rows):
            Hex(G, c, r, a)

    # 2. deleting duplicated nodes and edges (indexes repairing):
    Temp = list(set(G.nodes))
    for e, edge in enumerate(G.edges):
        i1, i2 = edge[0], edge[1]
        tuple1, tuple2 = G.nodes[i1], G.nodes[i2]
        newidx1, newidx2 = Temp.index(tuple1), Temp.index(tuple2)
        for j, face in enumerate(G.faces):
            if edge in face:
                idx = G.faces[j].index(edge)
                G.faces[j][idx] = (newidx1, newidx2)
        G.edges[e] = (newidx1, newidx2)
    G.nodes = Temp
    G.edges = list(set(tuple(sorted(l)) for l in G.edges))


# creating graph F which is dual to G, grid of possible ways (red graph)
def DualGraph(G: Graph):
    F = Graph()
    a = 5
    # 1. Defining nodes, by computing center of each face
    for face in G.faces:
        x = 0
        y = 0
        Nodes = []
        for edge in face:
            node1 = G.nodes[edge[0]]
            node2 = G.nodes[edge[1]]
            if node1 not in Nodes:
                Nodes.append(node1)
                x += Nodes[-1][0]
                y += Nodes[-1][1]
            if node2 not in Nodes:
                Nodes.append(node2)
                x += Nodes[-1][0]
                y += Nodes[-1][1]
        x /= len(face)
        y /= len(face)
        F.addNode(x, y)

    # 2. Defining edges with k-nearest neighbours algorithm
    for node in F.nodes:
        nodeidx = F.nodes.index(node)
        k = []  # nearest nodes indexes
        distances = []
        for n in F.nodes:
            if n == node:
                continue
            d = (node[0] - n[0]) ** 2 + (node[1] - n[1]) ** 2
            distances.append(d)
            k.append(F.nodes.index(n))
            if len(k) > 6:
                idx = distances.index(max(distances))
                del k[idx]
                del distances[idx]
        for idx in k:
            if np.sqrt(distances[k.index(idx)]) < 3 * a:
                F.addEdge(nodeidx, idx)

    F.edges = list(set(tuple(sorted(l)) for l in F.edges))  # deleting duplicates
    return F


# creating the actual maze, forming possible moving ways in planar graph with randomized depth-breadth search algorithm
def Maze(F: Graph):
    # 1. Choosing random cell
    idx = rd.randint(0, len(F.nodes) - 1)
    Visited = [idx]
    Backtracking = [idx]  # contains information about the solution
    journey = []
    # 2. While any node is unvisited
    while len(Visited) != len(F.nodes):
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
            rdn = rd.randint(0, len(ways) - 1)
            way = ways[rdn]
            ways.remove(way)
        else:  # dead end
            idx = Backtracking[-1]
            del Backtracking[-1]
            continue

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

        # 2.5 deleting unused edges
        for edge in F.edges:
            if edge[0] in Visited and edge[1] in Visited:
                if (edge[0], edge[1]) not in journey and (edge[1], edge[0]) not in journey:
                    F.edges.remove(edge)


# deleting walls (blue edges) if wall intersects with ways (red edges)
def DeleteIntersections(G: Graph, F: Graph):
    # for each way find wall which intersect this specific way and delete this specific wall
    for edge in F.edges:
        f1 = F.nodes[edge[0]]
        f2 = F.nodes[edge[1]]
        for e in G.edges:
            g1 = G.nodes[e[0]]
            g2 = G.nodes[e[1]]
            if doIntersect(f1, f2, g1, g2):
                G.edges.remove(e)
                break


# Algorithm:
Z = Graph()
# 1.
prepareGraph(Z, columns=16, rows=16)
# 2.
Zd = DualGraph(Z)
# 3.
Maze(Zd)
# 4.
DeleteIntersections(Z, Zd)

# plotting ways
for i in range(len(Zd.edges)):
    Zd.plotEdge(i, color='r')

# plotting walls
for i in range(len(Z.edges)):
    Z.plotEdge(i)
plt.show()