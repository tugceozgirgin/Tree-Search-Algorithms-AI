from typing import List
from Data import Data
from Node import Node
from PriorityQueue import PriorityQueue
from Solver import Solver, Solution

class UCS_iterative(Solver):
    """
    This is the Iterative UCS class.
    """
    def __init__(self, data: Data):
        super().__init__(data)
        self.priority_queue = PriorityQueue()
        self.optimal_sol = [self.data.depot_node]
        self.optimal_dist = float("inf")
        self.visited = set([self.data.depot_node])
        self.max_load = max(node.load for node in self.data.nodes if node.is_store)
        self.iteration = 0
        self.memo = {}

    
    def solve(self) -> Solution:
        self.priority_queue.enqueue(([self.data.depot_node],0,0), 0)

        while not self.priority_queue.is_empty():
            prior_track, prior_track_cost, prior_track_load = self.priority_queue.dequeue()
            expanding_node = prior_track[-1]
             
            # Memoization check 
            nodes_set = frozenset(node.id for node in prior_track)
            memo_key =(nodes_set, prior_track_load)

            if memo_key in self.memo and self.memo[memo_key]<= prior_track_cost:
                continue
            self.memo[memo_key] = prior_track_cost
           
            min_return_cost = min([self.data.get_distance(expanding_node, self.data.depot_node)] + [self.data.get_distance(expanding_node, n) for n in self.data.nodes if n not in self.visited])
            if prior_track_cost+ min_return_cost  >= self.optimal_dist:
               continue

            if self.is_all_visited(prior_track):
                prior_track = prior_track + [self.data.depot_node]
                prior_track_cost = prior_track_cost + self.data.get_distance(expanding_node,self.data.depot_node)
                if prior_track_cost < self.optimal_dist and self.data.is_feasible(prior_track):
                    self.optimal_sol = list(prior_track)
                    self.optimal_dist = prior_track_cost
                    continue

            self.iteration+=1
            # successors = sorted(
            #    (node for node in self.data.nodes if node not in prior_track or node.is_depot),
            #   key=lambda node: self.data.get_distance(expanding_node, node)
            # )
            for successor in self.data.nodes:
                if successor == expanding_node:
                    continue
                if successor not in prior_track or successor.is_depot:
                    new_obj_func = prior_track_cost + self.data.get_distance(expanding_node,successor)
                    
                    if new_obj_func >= self.optimal_dist:
                        continue
                    
                    new_load = prior_track_load + successor.load

                    if new_load > self.data.vehicle_capacity:
                        continue

                    if successor.is_store and new_load <= self.data.vehicle_capacity:
                        new_track = prior_track + [successor]
                        self.visited.add(expanding_node)
                        self.priority_queue.enqueue((new_track,new_obj_func,new_load),new_obj_func)
                            
                    elif successor.is_depot:# and new_load + self.max_load > self.data.vehicle_capacity: 
                        new_track = prior_track + [successor]
                        self.visited.add(expanding_node)
                        self.priority_queue.enqueue((new_track,new_obj_func,0),new_obj_func)
         
        print("Iterations:", self.iteration)
        return self.optimal_sol
    
    def is_all_visited (self, track: List[Node]) -> bool:
        return set(self.data.store_nodes).issubset(set(track))
    