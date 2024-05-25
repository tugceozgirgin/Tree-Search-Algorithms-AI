# Tree Search Algorithms-AI
 Three tree-search algorithms—Depth First Search (DFS), Uniform Cost Search (UCS), and A*—that were used to solve the Capacitated Single Vehicle Routing Problem (CSVRP) in a limited urban delivery scenario are developed
 
Three different tree-search algorithms, namely Depth First Search (DFS), Uniform Cost Search (UCS), and A* Search, were put into practice and assessed in order to tackle these issues. These algorithms provide distinct methods for pathfinding in weighted graphs and are all quite pertinent to the current issue:

1. DFS: Depth First Search (DFS) offers a comprehensive, albeit computationally costly,way to look at every potential path by traveling as far as feasible down each branch before turning around.
2. UCS: To identify the least expensive route in a weighted graph, Uniform Cost Search (UCS) extends the least expensive node first, guaranteeing that the shortest paths are taken into consideration incrementally.
3. A*: By including a heuristic function that calculates the cost from the current node to the objective, A* Search improves UCS by choosing paths that are most likely to arrive at the best answer swiftly and effectively.

Across three predefined scenarios of fully connected and directed graphs with varying complexity (small, medium, and large graphs), the efficacy of these algorithms was assessed based on multiple
performance metrics, including computational time, optimality of the solution (minimum total traveldistance), and the number of nodes expanded during the search. Below there is a visual representation of the small graph that has been used to test search algorithms:

   ![image](https://github.com/tugceozgirgin/Tree-Search-Algorithms-AI/assets/93055813/5722cb63-2129-4b16-8b3b-8873caa7020c)

![image](https://github.com/tugceozgirgin/Tree-Search-Algorithms-AI/assets/93055813/618293db-38fe-4c04-91fc-dbcef96fcb78)
