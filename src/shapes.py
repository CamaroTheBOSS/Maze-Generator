from graph import Graph


# creates one hexagon
def Hex(G: Graph, column, row, a):
    # 1. Defining starting point
    if (row + 1) % 2 == 0:
        x = (2 * column + 1) * a
    else:
        x = 2 * column * a
    y = -1.5 * row * a

    # 2. Defining Hex shape
    shiftX = [a, 0, -a, -a, 0, a]
    shiftY = [0.5*a, a, 0.5*a, -0.5*a, -a, -0.5*a]
    Face = []

    # 3. Adding Nodes and Edges
    G.addNode(x, y)
    for k in range(5):
        x += shiftX[k]
        y += shiftY[k]
        G.addNode(x, y)
        G.addEdge(len(G.nodes) - 1, len(G.nodes) - 2)
        Face.append(G.edges[-1])
    G.addEdge(len(G.nodes) - 1, len(G.nodes) - 6)
    Face.append(G.edges[-1])
    G.addFace(Face)
