from typing import List
from Data import Data
from Node import Node
from PriorityQueue import PriorityQueue
from Solver import Solver, Solution

class AStar_itearative(Solver):
    """
    This is the iterative class for AStar algorithm
    """
    def __init__(self, data: Data):
        super().__init__(data)
        self.priority_queue = PriorityQueue()
        self.optimal_sol = [self.data.depot_node]
        self.optimal_dist = float("inf")
        self.iteration = 0
        self.memo = {}
    
    def solve(self) -> Solution:
        self.priority_queue.enqueue(([self.data.depot_node],0,0), 0)
        visited = set([self.data.depot_node.id])

      
        while not self.priority_queue.is_empty():
            prior_track, prior_track_cost, prior_track_load = self.priority_queue.dequeue()
            expanding_node = prior_track[-1]

            # Memoization check 
            nodes_set = frozenset(node.id for node in prior_track)
            memo_key =(nodes_set, prior_track_load)

            if memo_key in self.memo and self.memo[memo_key]<= prior_track_cost:
                continue
            self.memo[memo_key] = prior_track_cost
            
            min_return_cost = min([self.data.get_distance(expanding_node, self.data.depot_node)] + [self.data.get_distance(expanding_node, n) for n in self.data.nodes if n not in visited])

            if prior_track_cost + min_return_cost >= self.optimal_dist:
               continue


            if self.is_all_visited(prior_track):
                prior_track = prior_track + [self.data.depot_node]
                prior_track_cost = prior_track_cost + self.data.get_distance(expanding_node,self.data.depot_node)
                if prior_track_cost < self.optimal_dist and self.data.is_feasible(prior_track):
                  self.optimal_sol = list(prior_track)
                  self.optimal_dist = prior_track_cost
                  continue
            
            self.iteration+=1
            for successor in self.data.nodes:
                if successor == expanding_node:
                    continue
                if successor not in prior_track or successor.is_depot:
                    # g(n) +f(n)
                    #new_obj_func = prior_track_cost + self.data.get_distance(expanding_node,successor)
                    #new_heuristic_cost = self.min_span_tree_heuristic(successor, prior_track + [successor],data)
                    new_track = prior_track + [successor]
                    gn = self.data.calculate_objective(new_track)
                    fn = self.shortest_path_heuristic(successor, [node for node in self.data.store_nodes if node not in prior_track])
                    new_obj_func = gn +fn

                    if new_obj_func >= self.optimal_dist:
                        continue
                    
                    new_load = prior_track_load + successor.load

                    if successor.is_store and new_load <= self.data.vehicle_capacity:
                        visited.add(expanding_node) 
                        self.priority_queue.enqueue((new_track,new_obj_func,new_load),new_obj_func)
                        
                    elif successor.is_depot: # and new_load + min_load > self.data.vehicle_capacity: 
                        visited.add(expanding_node)
                        self.priority_queue.enqueue((new_track,new_obj_func,0),new_obj_func)
            
        print("Iterations:", self.iteration)
        return self.optimal_sol
    

    def is_all_visited (self, track: List[Node]) -> bool:
        return set(self.data.store_nodes).issubset(set(track))
     
    def shortest_path_heuristic(self, initial_node, unvisited_nodes):
        #This heuristic approach uses the Dijkstra shortest path algorithm to find shortest path between unvisited nodes
        priorty_queue = PriorityQueue()
        priorty_queue.enqueue((initial_node,0),0)
        edges = {node.id: float('inf') for node in unvisited_nodes}
        edges[initial_node.id] = 0 
        unvisited_nodes += [initial_node]

        while not priorty_queue.is_empty():
            node, node_cost = priorty_queue.dequeue()
            for neighbor_node in unvisited_nodes:
                cost_of_edge = node_cost + self.data.get_distance(node,neighbor_node)
                if cost_of_edge < edges[neighbor_node.id]:
                    edges[neighbor_node.id] = cost_of_edge
                    priorty_queue.enqueue((neighbor_node,cost_of_edge), cost_of_edge)
        
        shortest_path = sum(edges[node.id] for node in unvisited_nodes if node.id in edges)
        return shortest_path
   

    
    def minimum_spanning_tree_heuristic(self,current_node, unvisited_nodes):
        #This Heuristic approach uses Prim's algorithm to calculate minimum spanning tree between unvisited nodes.
        min_cost = 0
        edges = PriorityQueue()
        visited_nodes = set()
        visited_nodes.add(current_node.id)

        for node in self.data.nodes:
            if node.id != current_node.id and node in unvisited_nodes:
              edge_cost =self.data.get_distance(current_node, node)
              edges.enqueue((node,edge_cost), edge_cost) 
        while edges:
          node, cost = edges.dequeue()
          if node.id not in visited_nodes:
              visited_nodes.add(node)
              min_cost += cost
              for next_node in self.data.nodes:
                  if next_node.id not in visited_nodes and next_node in unvisited_nodes:
                      edges.enqueue((next_node, self.data.get_distance(node, next_node)), self.data.get_distance(node, next_node))
        return min_cost

    







   