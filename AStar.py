from typing import List
from Data import Data
from Node import Node
from PriorityQueue import PriorityQueue
from Solver import Solver, Solution

class AStar(Solver):
    """
    This is the recursive class of A* algorithm
  
    """
    def __init__(self, data: Data):
        super().__init__(data)
        self.priority_queue = PriorityQueue()
        self.optimal_sol = [self.data.depot_node]
        self.optimal_dist = float("inf")
        self.iteration = 0
        self.memo ={}
    
    def solve(self) -> Solution:
        self.priority_queue.enqueue([self.data.depot_node],0)
        visited = set([self.data.depot_node])
        self.astar(0,0,visited)
        print("Iterations:", self.iteration)
        return self.optimal_sol
    
    def astar(self, cumulative_load: float, total_dist: float, visited: set):
        if self.priority_queue.is_empty():
            return
        
        prior_track = self.priority_queue.dequeue()
        expanding_node = prior_track[-1]

        # Memoization check 
        nodes_set = frozenset(node.id for node in prior_track)
        memo_key =(nodes_set, cumulative_load)

        if memo_key in self.memo and self.memo[memo_key]<= total_dist:
            return
        self.memo[memo_key] = total_dist
            
        min_return_cost = min([self.data.get_distance(expanding_node, self.data.depot_node)] + [self.data.get_distance(expanding_node, n) for n in self.data.nodes if n not in visited])

        if total_dist + min_return_cost >= self.optimal_dist:
            return

        if self.is_all_visited(prior_track):
                prior_track = prior_track + [self.data.depot_node]
                prior_track_cost = total_dist + self.data.get_distance(expanding_node,self.data.depot_node)
                if prior_track_cost < self.optimal_dist and self.data.is_feasible(prior_track):
                    self.optimal_sol = list(prior_track)
                    self.optimal_dist = prior_track_cost
                    return
                
        self.iteration+=1            
        for successor in self.data.nodes:
            if successor == expanding_node:
                continue
            
            if successor in visited and successor != self.data.depot_node:
                continue

            new_track = prior_track + [successor]
            gn = self.data.calculate_objective(new_track)
            fn = self.shortest_path_heuristic(successor, [node for node in self.data.store_nodes if node not in prior_track])
            new_obj_func = gn +fn

            if new_obj_func >= self.optimal_dist:
                continue

            new_visited = visited.copy()
            new_visited.add(successor)
            new_load = cumulative_load + successor.load

            if successor.is_store and new_load <= self.data.vehicle_capacity:
                self.priority_queue.enqueue(new_track, new_obj_func)
                self.astar(cumulative_load + successor.load, new_obj_func, new_visited)

            elif successor.is_depot:
                self.priority_queue.enqueue(new_track, new_obj_func)
                self.astar(0, new_obj_func, new_visited)
    

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
    



