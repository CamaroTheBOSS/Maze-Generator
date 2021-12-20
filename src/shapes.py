from graph import Graph


# Building Structure Function
def BuildShape(G: Graph, x, y, shiftX, shiftY, v=6):
    # 1. Adding Nodes (Added list is because we do not want to add duplicated nodes and edges)
    Added = []
    if (x, y) not in G.nodes.values():
        G.addNode(x, y)
    Added.append((x, y))
    for k in range(v - 1):
        x += shiftX[k]
        y += shiftY[k]
        if (x, y) not in G.nodes.values():
            G.addNode(x, y)
        Added.append((x, y))

    # 2. Adding Edges and Faces
    Face = []
    for i in range(len(Added)):
        value1 = Added[i - 1]
        value2 = Added[i]

        idx1 = list(G.nodes.keys())[list(G.nodes.values()).index(value1)]
        idx2 = list(G.nodes.keys())[list(G.nodes.values()).index(value2)]

        if idx2 not in G.edges[idx1]:
            G.edges[idx1].append(idx2)
        if idx1 not in G.edges[idx2]:
            G.edges[idx2].append(idx1)

        Face.append(idx2)
    G.faces.append(Face)


# Hexagon shape
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

    # 2. Build Structure
    BuildShape(G, x, y, shiftX, shiftY, v=6)


# Triangle shape
def Triangle(G: Graph, column, row, a):
    h = 0.9 * a
    # 1. Defining starting point and shape
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

    # 2. Build Structure
    BuildShape(G, x, y, shiftX, shiftY, v=3)


# Square shape
def Square(G: Graph, column, row, a):
    # 1. Defining shape
    x = a * column
    y = - a * row

    shiftX = [a, 0, -a, 0]
    shiftY = [0, -a, 0, a]

    # 2. Build Structure
    BuildShape(G, x, y, shiftX, shiftY, v=4)
