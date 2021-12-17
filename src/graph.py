import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.faces = []

    def addNode(self, x, y):  # takes coordinates
        self.nodes.append((x, y))

    def addEdge(self, nidx1: int, nidx2: int):  # takes nodes indexes
        if len(self.nodes) > nidx1 and len(self.nodes) > nidx2:
            self.edges.append((nidx1, nidx2))

    def addFace(self, edges: list):
        self.faces.append(edges)

    def plotEdge(self, k, color='b'):
        nidx1 = self.edges[k][0]
        nidx2 = self.edges[k][1]
        x = [self.nodes[nidx1][0], self.nodes[nidx2][0]]
        y = [self.nodes[nidx1][1], self.nodes[nidx2][1]]

        plt.plot(x, y, color)
