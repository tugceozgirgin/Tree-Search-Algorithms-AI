from typing import Optional
from Data import Data
from Solver import Solver, Solution
from random import Random


class RandomSolver(Solver):
    """
        This class employs a random approach
    """

    seed: Optional[int]  #: Random seed

    def __init__(self, data: Data, seed: Optional[int] = None):
        super().__init__(data)

        self.seed = seed

    def solve(self) -> Solution:
        """
            Making random assignments

            :return: A random solution
        """

        # Create random object
        rnd = Random(self.seed) if self.seed is not None else Random()

        # Initiate variables
        cumulative_load = 0.

        visited_nodes = set()

        # Initiate solution
        solution = [self.data.depot_node]

        #print("Lenght of nodes: ", len(self.data.nodes))

        while not self.data.is_feasible(solution):  # Until a feasible solution is found.
            # Define candidate (i.e., unvisited) stores
            candidate_stores = [store_node for store_node in self.data.store_nodes if store_node not in visited_nodes]
            
            #for node in candidate_stores:
             #   print(f"Cand store : {node.id}")

            # If all stores are visited
            if len(candidate_stores) == 0:
                solution.append(self.data.depot_node)
                continue

            # Randomly select the next node
            select_store = rnd.choice(candidate_stores)
            #print("Selceted store ", select_store.id)

            # Check remaining capacity
            if select_store.load > self.data.vehicle_capacity - cumulative_load:
                solution.append(self.data.depot_node)
                #print("out of capacity")
                cumulative_load = 0

            # Visit the node
            solution.append(select_store)
            visited_nodes.add(select_store)
            cumulative_load += select_store.load
        
        # for node in solution:
        #     print(f"Solution : {node.id}")

        return solution
