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
        print(k)
        x += shiftX[k]
        y += shiftY[k]
        G.addNode(x, y)
        G.addEdge(len(G.nodes) - 1, len(G.nodes) - 2)
        Face.append(G.edges[-1])
    G.addEdge(len(G.nodes) - 1, len(G.nodes) - 6)
    Face.append(G.edges[-1])
    G.addFace(Face)


def Triangle(G: Graph, column, row, a):
    h = 0.9 * a
    if (column + 1) % 2 == 0 and (row + 1) % 2 == 0:  # column and row even
        y = -h * row
        x = a * column / 2
        shiftX = [a, -0.5 * a, -0.5 * a]
        shiftY = [0, h, -h]
    elif (column + 1) % 2 == 0 and (row + 1) % 2 == 1:  # column even, row odd
        x = a * column / 2
        y = -h * (row - 1)
        shiftX = [a, -0.5 * a, -0.5 * a]
        shiftY = [0, -h, +h]
    elif (column + 1) % 2 == 1 and (row + 1) % 2 == 0:  # column odd, row even
        x = a * column / 2
        y = -h * (row - 1)
        shiftX = [a, -0.5 * a, -0.5 * a]
        shiftY = [0, -h, +h]
    elif (column + 1) % 2 == 1 and (row + 1) % 2 == 1:  # column and row odd
        x = a * column / 2
        y = -h * row
        shiftX = [a, -0.5*a, -0.5*a]
        shiftY = [0, h, -h]
    Face = []

    G.addNode(x, y)
    for k in range(2):
        x += shiftX[k]
        y += shiftY[k]
        G.addNode(x, y)
        G.addEdge(len(G.nodes) - 1, len(G.nodes) - 2)
        Face.append(G.edges[-1])
    G.addEdge(len(G.nodes) - 1, len(G.nodes) - 3)
    Face.append(G.edges[-1])
    G.addFace(Face)