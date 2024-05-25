from typing import List
from Data import Data
from Node import Node
from PriorityQueue import PriorityQueue
from Solver import Solver, Solution

class UCS(Solver):
    """
    This is the recusive UCS CLASS.

    This is an recursive approach for Uniform Cost Search algorithm. It is much more faster than iterative approach in UCS_iterative.py.
    """
    def __init__(self, data: Data):
        super().__init__(data)
        self.priority_queue = PriorityQueue()
        self.optimal_sol = [self.data.depot_node]
        self.optimal_dist = float("inf")
        self.min_load = min(node.load for node in self.data.nodes if node.is_store)
        self.max_load = max(node.load for node in self.data.nodes if node.is_store)
        self.iteration = 0
        self.memo = {}
    
    def solve(self) -> Solution:
        self.priority_queue.enqueue([self.data.depot_node],0)
        visited = set([self.data.depot_node])
        self.ucs(0,0,visited)
        print("Iterations: ", self.iteration)
        return self.optimal_sol
    
    def ucs(self, cumulative_load: float, total_dist: float, visited: set):
        if self.priority_queue.is_empty():
            return
        
        prior_track = self.priority_queue.dequeue()
        expanding_node = prior_track[-1]

        #Memoization
        nodes_set = frozenset(node.id for node in prior_track)
        memo_key =(nodes_set, cumulative_load)

        if memo_key in self.memo and self.memo[memo_key]<= total_dist:
            return
        self.memo[memo_key] = total_dist

        min_return_cost = min([self.data.get_distance(expanding_node, self.data.depot_node)] + [self.data.get_distance(expanding_node, n) for n in self.data.nodes if n not in visited])

        if total_dist + min_return_cost  >= self.optimal_dist:
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

            new_obj_func = total_dist + self.data.get_distance(expanding_node,successor)
            
            if new_obj_func >= self.optimal_dist:
                continue

            new_visited = visited.copy()
            new_visited.add(successor)
            new_track = prior_track + [successor]
            new_load = cumulative_load + successor.load

            if successor.is_store and new_load <= self.data.vehicle_capacity:
                self.priority_queue.enqueue(new_track, new_obj_func)
                self.ucs(cumulative_load + successor.load, new_obj_func, new_visited)

            elif successor.is_depot: # and new_load + self.max_load > self.data.vehicle_capacity:
                self.priority_queue.enqueue(new_track, new_obj_func)
                self.ucs(0, new_obj_func, new_visited)
    

    def is_all_visited (self, track: List[Node]) -> bool:
        return set(self.data.store_nodes).issubset(set(track))

