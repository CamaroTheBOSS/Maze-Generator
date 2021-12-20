import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.faces = []

    def addNode(self, x, y):  # takes coordinates
        self.nodes[len(self.nodes)] = (x, y)
        self.edges[len(self.nodes) - 1] = []

    def addEdge(self, nidx1: int, nidx2: int):  # takes nodes indexes
        if len(self.nodes) > nidx1 and len(self.nodes) > nidx2:
            self.edges[nidx1].append(nidx2)

    def addFace(self, nodes):
        self.faces.append(nodes)

    def plotGraph(self, color='b'):
        # 1. to not duplicated the edges and improve optimization if node
        Added = []
        for k in self.nodes:
            x, y = [], []
            if k in Added:
                continue
            for node in self.edges[k]:
                if node in Added:
                    continue
                x.append(self.nodes[k][0])
                y.append(self.nodes[k][1])
                x.append(self.nodes[node][0])
                y.append(self.nodes[node][1])
            Added.append(k)
            plt.plot(x, y, color)
