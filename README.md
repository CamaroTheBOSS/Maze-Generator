# Maze-Generator
Maze generator with most popular shapes - hexagon, triangle, square:


1. Theory: 

- Planar Graph https://en.wikipedia.org/wiki/Planar_graph
Its role is to make the structure of the maze. In this graph information is stored information about nodes, edges and faces of the grid. Nodes are (x, y) points position,
edges (a, b) contains indexes of nodes which create specific edge. Faces are a lists of lists of edges [(a, b), (b, c), ..., (f, a)] which create specific face. 

- Dual Graph https://en.wikipedia.org/wiki/Dual_graph
Its role is to make the grid of the possible moves between cells (faces of the planar graph)

- k-nearest neighbour algorithm https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm
Is used for determining neighbour cells for each cell

- randomized depth-first search algorithm https://en.wikipedia.org/wiki/Maze_generation_algorithm
Is used for determining possible moving ways in the maze. It is just one of many possibilities to make ways. I choosed recursive implementation

- edges intersection https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
Testing wheter edges are intersecting using vectors theory. Orientation of two vectors (edges) is computed and is tested whether intersect point is a part of the segments.
Implementation is took from the link. It is neccessary to test whether planar graph's wall is intersecting with possible way (dual graph's edges). If yes, wall is deleted.

2. Idea:

- Program is built based on graph theory. Maze is made of two graphs. The idea is to make a planar graph which creates grid of shapes (hexagons, triangles etc.) and create
another graph which is dual to the first graph. The role of this second graph is to create possible moving ways in the maze. This graph has nodes in the centers of faces
defined by the planar graph and edges, which connecting every neighbour face with k-nearest neighbour algorithm. The next step is to run Randomized depth-first search
algorithm which travels around the dual graph and creates actual maze. The last step is to delete walls which are intersected by the edges of the dual graph.

3. Program's structure:

  3.1 In first step the planar graph is constructed with possibility to change the number of columns and rows of the maze. This creates a structure of the maze (e.g. 10x10):
  
  ![image](https://user-images.githubusercontent.com/67116759/146556239-2262c6b0-f20d-42b8-ba7f-0af32c20296d.png)
  
   - In prepareGraph() function is called Hex() function (columns * rows) times which creates (columns * rows) hexagons. Hex() called multiple times creates duplicated nodes
   and edges in the graph which is undesirable, so in the next part of the prepareGraph function duplicated nodes are removed and the edges indexes are repaired (because
   after deleting some nodes, edges has references to nodes which actually do not exist (look 1. Theory links))
  
  3.2 Second step is construction dual graph to the planar graph. It creaetes structure of the possible moves to choose by the algorithm (red one, case 10x10):
  
  ![image](https://user-images.githubusercontent.com/67116759/146559418-7f6f4f2d-f8a8-4b3d-afbb-8aaf4f59dceb.png)
  
  - Dual graph F is created in DualGraph() function which takes another Graph G which it will be dual to. Nodes of graph F are computed by calculating center of each face
  in graph G ((average(sum(each x)), average(sum(each y)), each x and y from all nodes which create specific face). After that, edges are defined with k-nearest-neighbours
  algorithm. It takes 6 nearest candidates to be a neighbour and make edge between nodes which are in distance < 3 * a. Thats because not every node has 6 neighbours,
  so this restriction decreasing number of neighbours for side hexagons.
  
  3.3 Next step is to make actual maze. To do this I used randomized depth-first search algorithm (one of many possibilities, one of the easiest and which gives simplest mazes):
  
  ![image](https://user-images.githubusercontent.com/67116759/146561552-0d0a841f-d007-49bc-ac2e-8f3aae4f496e.png)
  
  - Firstly, algorithm selects random node from dual graph (red one) and marks it as visited and add it to possible backtrack. Then it makes list with possible ways (edges)
  to unvisited nodes and selects random way. If unvisited node in nearest neighbourhood does not exists (dead end) it backtracks (move to the last node at the 
  backtrack list and removes this node from this list). If unvisited node or nodes exist algorithm selects it randomly and marks new node to the visited nodes. Then
  add this node to the "Backtrack" list and add selected way to the "journey" list which contains traveled ways. After each completed iteration (without dead ends)
  algorithm checks for all the edges if the nodes which are connected by the edge are both visited. If yes, it tests if this edge is in the "journey". If not, it can
  be deleted.
  
  3.4 Last step is to delete walls between cells connected by dual graph's edges (10x10 case):
  
  ![image](https://user-images.githubusercontent.com/67116759/146563641-6cd952ed-c012-4032-b93b-3f4e075fb62a.png)
  
  - Function DeleteIntersections() deletes all the walls (planar graph's edges) which are intersecting with the ways (dual graph's edges). For every edge in dual graph
  it takes every edge in planar graph and tests whether the edges intersect. If yes, the wall is deleted and another way is took to test (because way could intersect
  with only one wall so it has no sense to continue this iteration). To tell if the edges are intersected I use functions doIntersect() which uses orientation(), which
  returns orientation of the given vectors, and onSegment which tells us whether the intersect point is in the range of the vectors.
  
  3.5 In addition I created a pathfinder which takes given startnode and goalnode. It works with Breadth First Search Algorithm. This is algorithm.
  
  ![image](https://user-images.githubusercontent.com/67116759/146687366-d69a08d8-d5c4-4e5d-a927-df8a86a5abfb.png)
  
4. Some information

- It is possible to turn off display of the dual graph (ways), just comment last but one for loop

![image](https://user-images.githubusercontent.com/67116759/146567693-fbc120fd-6417-4edb-95c4-5378ed3f3fab.png)

- Program is inefficient for large mazes (32x32 is constructing 30sec), so it is recommended to test program for max 20x20 size :)
- Changing shape's edge size to enough small value (a = 1) could cause some bugs in dual graph's structure
- To get the best effect in triangle maze call prepareGraph with columns and rows values in ratio 3:2 (18x12, 24x16 etc.)

  ![image](https://user-images.githubusercontent.com/67116759/146642946-04428302-f13e-4d34-878a-1060f6a39599.png)
  


  
