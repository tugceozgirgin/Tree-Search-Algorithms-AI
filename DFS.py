from typing import List
from Data import Data
from Node import Node
from Solver import Solver, Solution


class DFS(Solver):
    """
        For the Assignment 1, you need to implement your *Depth First Search* (DFS) algorithm to solve VRP problem in
        this class.

        >> *Note*: You are free to make changes (i.e., defining variables and methods) in this class.
    """

    def __init__(self, data: Data):
        super().__init__(data)
        self.optimal_sol = [self.data.depot_node]
        self.optimal_dist = float("inf")
        self.visited = set([self.data.depot_node])
        self.max_load = max(node.load for node in self.data.nodes if node.is_store)
        #self.min_load = min(node.load for node in self.data.nodes if node.is_store)
        self.iteration = 0
        self.memo = {}

    def solve(self) -> Solution:
        """
            TODO: Implement DFS algorithm to solve VRP problem.

            This method must provide the **solution** as a sequence (``Sequence[Node]``).

            :return: Solution found by DFS
        """
        self.dfs([self.data.depot_node],0,0)
        print("Iterations: ", self.iteration)
        return self.optimal_sol
    
    
    def dfs(self, track:List[Node], total_dist: float, cumulative_load: float):

        # Memoization check
        nodes_set = frozenset(node.id for node in track)
        memo_key =(nodes_set, cumulative_load)

        if memo_key in self.memo and self.memo[memo_key]<= total_dist:
            return
        self.memo[memo_key] = total_dist
 
        last_in_node = track[-1]
        min_return_cost = min([self.data.get_distance(last_in_node, self.data.depot_node)] + [self.data.get_distance(last_in_node, n) for n in self.data.nodes if n not in self.visited])
        
        #optimizasyon: gereksiz tracklere girme
        if total_dist + min_return_cost  >= self.optimal_dist:
            return
        
        #initial check is all nodes are visited
        if len(track) > 1 and last_in_node == self.data.depot_node and self.is_all_visited(track):
            if total_dist < self.optimal_dist:
                if self.data.is_feasible(track):
                    self.optimal_sol = list(track)
                    self.optimal_dist = total_dist
            return
        
        self.iteration+=1 
        #Expand
        nodes_to_check = [ node for node in self.data.nodes if node not in track or node.is_depot]
        for successor_node in nodes_to_check:
            if successor_node not in track or successor_node == self.data.depot_node:
                if successor_node == last_in_node:
                    continue
                distance = self.data.get_distance(last_in_node, successor_node)

                if total_dist + distance >= self.optimal_dist:
                  continue

                new_load = cumulative_load + successor_node.load

                if new_load > self.data.vehicle_capacity:
                    continue
            
                if successor_node.is_store and new_load <= self.data.vehicle_capacity:
                    track.append(successor_node)
                    self.dfs(track, total_dist + distance , cumulative_load + successor_node.load)
                    self.visited.add(last_in_node)
                    track.pop()
                 
                elif successor_node.is_depot and new_load + self.max_load > self.data.vehicle_capacity:
                    track.append(successor_node)
                    self.dfs(track, total_dist + distance , 0)
                    self.visited.add(last_in_node)
                    track.pop()



    def is_all_visited (self, path: List[Node]) -> bool:
        store_nodes = set(self.data.store_nodes)
        for store in store_nodes:
            if store not in path:
                return False
        return True



