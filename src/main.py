import numpy as np
import random as rd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from shapes import *
from intersect import *
from finder import *


# Author: Kacper Plesiak
# it is worth to read README.md file at https://github.com/CamaroTheBOSS/Maze-Generator

# constructing grid of cells (blue graph) with given shape (not implemented yet) and size
def prepareGraph(G: Graph, columns: int = 5, rows: int = 5, shape='Hexagon'):  # a - edgeSize
    a = 5
    # 1. preparing shapes:
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


# creating graph F which is dual to G, grid of possible ways (red graph)
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

    # 2. Defining edges with k-nearest neighbours algorithm
    neighnum = len(G.faces[0])
    if neighnum == 6:
        condition = 3 * a
    elif neighnum == 3:
        condition = 0.95 * a
    elif neighnum == 4:
        condition = 1.1 * a

    for key, node in F.nodes.items():

        k = []  # nearest nodes indexes
        for kn, n in F.nodes.items():
            if n == node:
                continue
            d = abs(node[0] - n[0]) + abs(node[1] - n[1])
            if d < condition:
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
    ToDelete = [idx]  # candidates to delete unused edges
    Backtracking = [idx]  # contains information about the solution
    journey = []

    # 2. While any node is unvisited
    while len(Visited) != len(F.nodes):
        # 2.1 determining possible ways (to unvisited neighbours)
        ways = []
        for e in F.edges[idx]:
            if e in Visited and idx in Visited:
                pass
            else:
                ways.append((idx, e))

        # 2.2 choose one randomly (if dead end facilitate backtracking)
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

        # 2.4 track the journey of algorithm to have information about edges we must not delete
        journey.append(way)

    # 3. Delete unused edges
    for key, neighbours in F.edges.items():

        ToRemove = []
        for node in neighbours:
            if (key, node) not in journey and (node, key) not in journey:
                ToRemove.append(node)

        for element in ToRemove:
            F.edges[key].remove(element)
            F.edges[element].remove(key)


# deleting walls (blue edges) if wall intersects with ways (red edges)
def DeleteIntersections(G: Graph, F: Graph):
    # for each way find wall which intersect this specific way and delete this specific wall
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
prepareGraph(Z, columns=32, rows=32, shape='Hexagon')
# 2.
Zd = DualGraph(Z)
# 3.
Maze(Zd)
# 4.
DeleteIntersections(Z, Zd)

# Search Algorithm BFS from node 0 to node 32*32 - 1 (last one)
S = Graph()
S.nodes = Zd.nodes.copy()
S.edges = BreadthFirstSearch(Zd, 0, 32*32-1)

# Plotting
Z.plotGraph()
Zd.plotGraph(color='k')
S.plotGraph(color='r')

plt.show()
