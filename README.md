# Maze-Generator
Maze generator with most popular shapes - hexagon, triangle, square:


1. Theory: 

- Planar Graph https://en.wikipedia.org/wiki/Planar_graph
Its role is to create the structure of the maze. In this graph is stored information about nodes, edges and faces of the grid. Nodes (x, y) are coordinates
stored in dictionary {index: (x, y) etc}. Edges a->b contains indexes of nodes which create specific edge. Edges are stored in dictionary too: 
{a: [b, c]} (edges a->b and a->c). Faces are lists which contains all nodes which create specific face. 

- Dual Graph https://en.wikipedia.org/wiki/Dual_graph
Its role is to make the grid of the possible moves between cells (faces of the planar graph)

- k-nearest neighbour algorithm https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm
Is used for determining neighbour cells for each face

- randomized depth-first search algorithm https://en.wikipedia.org/wiki/Maze_generation_algorithm
Is used for determining possible moving ways in the maze. It is just one of many possibilities to create ways system.

- edges intersection https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
Testing wheter edges are intersecting using vectors theory. Orientation of two vectors (edges) is computed. Then is tested whether intersect point is a part of the
segments (vectors). Implementation is took from the link. It is used to delete walls beetween cells

2. Idea:

- Program is built based on graph theory. Maze is made of two graphs. The idea is to make a planar graph which creates grid of shapes (hexagons, triangles etc.) and then 
create another graph which is dual to the first graph. The role of this second graph is to create possible moving ways in the maze. This graph has nodes in the centers of 
faces defined by the planar graph and edges which connecting every neighbour face with k-nearest neighbour algorithm. The next step is to run Randomized depth-first search
algorithm which travels around the dual graph and creates actual maze. The last step is to delete walls which are intersected by the edges of the dual graph.

3. Program's structure:

  3.1 In first step the planar graph is constructed with possibility to change the number of columns and rows of the maze. This creates a structure of the maze (e.g. 10x10):
  
  ![image](https://user-images.githubusercontent.com/67116759/146556239-2262c6b0-f20d-42b8-ba7f-0af32c20296d.png)
  
   - In prepareGraph() function is called Hex() function (or another func) columns*rows times which creates columns*rows hexagons (or another shapes). This function called 
   multiple times creates pretty cool grid.
  
  3.2 Second step is to construct dual graph to the planar graph. It creaetes structure of the possible moves to choose by the algorithm (red one, case 10x10):
  
  ![image](https://user-images.githubusercontent.com/67116759/146559418-7f6f4f2d-f8a8-4b3d-afbb-8aaf4f59dceb.png)
  
  - Dual graph F is created in DualGraph() function which takes another Graph G it will be dual to. Nodes of graph F are computed by calculating center of each face
  in graph G (average coords from nodes which creates specific face). After that, edges are defined with k-nearest-neighbours
  algorithm. Not every node has the same number of neighbours, so it is important to restrict k-nearest-neighbours to search in specific radius. "Condition" variable is
  this radius.
  
  3.3 Next step is to make actual maze. To do this I used randomized depth-first search algorithm (one of many possibilities, one of the easiest and which gives simplest mazes):
  
  ![image](https://user-images.githubusercontent.com/67116759/146561552-0d0a841f-d007-49bc-ac2e-8f3aae4f496e.png)
  
  - Firstly, algorithm selects random node from dual graph (red one) and marks it as visited and add it to possible backtracking. Then it makes list with possible ways (edges)
  to unvisited nodes and selects random way. If unvisited node in nearest neighbourhood does not exists (dead end) it backtracks (move to the last node at the 
  "backtracking" list and removes this node from this list). If unvisited node or nodes exist algorithm selects it randomly and marks new node as visited. Then it
  adds this node to the "Backtracking" list and adds selected way to the "journey" list which contains traveled ways. After visiting every node the next step is to delete
  unused ways.
  
  3.4 Last step is to delete walls between cells connected by dual graph's edges (10x10 case):
  
  ![image](https://user-images.githubusercontent.com/67116759/146563641-6cd952ed-c012-4032-b93b-3f4e075fb62a.png)
  
  - Function DeleteIntersections() deletes all the walls (planar graph's edges) which are intersecting with the ways (dual graph's edges). For every way it takes 
  every edge in face it belongs to. Then intersection is tested. If edges intersect, the wall is deleted and another way is took to test (because way could intersect
  with only one wall so it has no sense to continue this iteration). To tell if the edges are intersected I use functions doIntersect() which uses orientation(), which
  returns orientation of the given vectors, and onSegment which tells us whether the intersect point is in the range of the vectors.
  
  3.5 In addition I created a pathfinder which takes given startnode and goalnode. It works with Breadth First Search Algorithm.
  
  ![image](https://user-images.githubusercontent.com/67116759/146687366-d69a08d8-d5c4-4e5d-a927-df8a86a5abfb.png)
  
4. Some information

- It is possible to turn off display of the dual graph (ways), just do not plot dualgraph (comment Gdual.plotGraph())

![image](https://user-images.githubusercontent.com/67116759/146567693-fbc120fd-6417-4edb-95c4-5378ed3f3fab.png)

- Program is inefficient for large mazes (80x80 is constructing 46sec), so it is recommended to test program for max 40x40 size :)
- To change the type of the maze for triangle maze or square change the "shape" arg to 'Triangle' or 'Square' in prepareGraph() function call
- To get the best effect in triangle maze call prepareGraph with columns and rows values in ratio 3:2 (18x12, 24x16 etc.)

  ![image](https://user-images.githubusercontent.com/67116759/146642946-04428302-f13e-4d34-878a-1060f6a39599.png)
  
 5. Big EDIT:
 - I was not satisfied of the optimization of this program so I decided to refactor it a little bit
 - In first version nodes and edges were lists and face list contained edge which creates specific face. Now nodes and edges are stored in dictionaries and face list
 contains every node which creates specific face. This change increased code readibility and created lots of new possibilities to improve optimization
 - Previously in prepareGraph() after creating a grid of shapes I had to remove duplicates of nodes and edges in grid and repair indexes in edges and faces 
 (because after deleting nodes some edges were containing wrong indexes). Now it is not neccessary because of the new, better code
 - In DualGraph() I improved k-nearest-neighbours algorithm. Previously it iterated through all the nodes (in every case) and choosed 6 (for Hexagon Maze) nearest nodes. After      that it checked whether these nodes distances are smaller than "condition" variable value. Now it iterate through the nodes and stops when it find 6 nearest neighbours, 
   because it checks whether node distance are smaller than "condition" variable regularly (it does not need to iterate through all the nodes but iterate until it find 6
   nodes which meet the condition)
 - In Maze() I could have deleted useless "if" conditions. It increased speed of the function, but most important thing I have done is to delete unused ways after visiting
   each node, so after "while loop". Previously algorithm was iterating through all the nodes to find a way to delete in every "while loop" iteration. This is powerful
   performace boost
 - In DeleteIntersections() previosly to find which wall is intersected by specific way, algorithm iterated through all the walls. Now it iterating only through the walls
   which are part of specific face (faces have the same indexes as the DualGraph nodes which are centers of specific face). Now this function is superfast.
 - Moreover some smallest improvments were added e.g. calculating static values before loops (previosly static values were calculated in each iteration)
 - In k-nearest-neighbours now is used abs(x1 - x2) func instead of sqrt((x1 - x2)^2). This is big improvment.
 - Below, I showed diffrences in optimization between first and second version of the program for 30x30 Hexagon Maze:
   
   ![image](https://user-images.githubusercontent.com/67116759/146843802-bcb9f0fb-3416-4012-8f63-50e8fc2046d2.png)
   
   ![image](https://user-images.githubusercontent.com/67116759/146843877-0e45481a-a440-4779-8cbe-52dd2b945065.png)
   
 - Only plotting is more complicated because the new structure of the program, but this is the cost for big performace boost in the other parts of the program
 - Below, I put a chart which shows duration of the program depending on the size of the grid (columns * rows value):

  ![image](https://user-images.githubusercontent.com/67116759/146845611-734ee8c4-dba8-4854-a40d-8d44babc5419.png)


 
  


  
