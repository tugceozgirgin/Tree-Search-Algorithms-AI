from __future__ import annotations
from random import Random
from typing import List, Optional, Union, Dict, TypeVar, Sequence
from Node import Node
import pickle as pkl


Solution = TypeVar("Solution", bound=Sequence[Node])
"""
    Solution format is a sequence, indicating the traveling path.
"""


class Data:
    """
        Data class holds the necessary parameters for the problem. Also, it can generate a random problem. Lastly,
        it can provide the validity (i.e., feasibility) and the objective value (i.e., max-span) of a given solution.
    """
    __distance_matrix: Dict[int, Dict[int, float]]  #: Distance matrix
    __nodes: List[Node]                             #: List of nodes
    __vehicle_capacity: float                       #: Vehicle load capacity

    def __init__(self, file_path: Optional[str] = None):
        """
            Constructor.
            If the file path is defined, it reads the parameters from the given pickle file. Otherwise, it initiates
            empty parameters.

            :param file_path: If the file
        """
        if file_path is not None:
            self.load(file_path)
        else:
            self.__nodes = []
            self.__distance_matrix = {}
            self.__vehicle_capacity = 0.

    def get_distance(self, node_source: Union[Node, int], node_target: Union[Node, int]) -> float:
        """
            This method provides the distance from *source* node to *target* node.

            :param node_source: The source *Node* object or node id.
            :param node_target: The target *Node* object or node id.
            :return: Distance from *source* node to *target* node
        """

        source_id = node_source if isinstance(node_source, int) else node_source.id
        target_id = node_target if isinstance(node_target, int) else node_target.id

        return self.__distance_matrix[source_id][target_id]

    def is_feasible(self, solution: Solution) -> bool:
        """
            This method checks the validity (i.e. feasibility) of a given solution.

            :param solution: Target solution
            :return: Whether the solution is feasible, or not.
        """
        # Visited nodes
        visited_nodes = set()
        visited_nodes.add(self.depot_node)

        # Cumulative load
        load = 0

        for i, node in enumerate(solution):
            if i == 0 and node.is_store:  # First node must be depot
                return False

            if i == len(solution) - 1 and node.is_store:  # Last node must be depot
                return False

            if node.is_depot:
                load = 0
            else:
                load += node.load

                if node in visited_nodes:  # Store nodes must be visited once
                    return False

            if load > self.__vehicle_capacity:  # Cumulative load amount cannot exceed the vehicle load capacity
                return False

            if node not in visited_nodes:
                visited_nodes.add(node)

        if len(visited_nodes) != len(self.__nodes):  # All nodes must be visited
            return False

        return True

    def calculate_objective(self, solution: Solution) -> float:
        """
            This method calculates the objective value (i.e., total travelling distance) of a given solution.

            :param solution: Target solution
            :return: Objective value
        """
        total_distance = 0.

        for i in range(1, len(solution)):
            total_distance += self.get_distance(solution[i - 1], solution[i])

        return total_distance

    @property
    def nodes(self) -> List[Node]:
        """
            This method provides the list of nodes in the current data

            :return: List of nodes
        """

        return self.__nodes

    @property
    def depot_node(self) -> Node:
        """
            This method provides the **depot** node

            :return: Depot node
        """

        for node in self.__nodes:
            if node.is_depot:
                return node

    @property
    def store_nodes(self) -> Sequence[Node]:
        """
            This method provides the **store** nodes

            :return: Store nodes
        """

        for node in self.__nodes:
            if node.is_store:
                yield node

    @property
    def vehicle_capacity(self) -> float:
        """
            This method provides the vehicle load capacity

            :return: Vehicle load capacity
        """

        return self.__vehicle_capacity

    def load(self, file_path: str):
        """
            Loading the data from a **pickle** file

            :param file_path: The path of the file
        """
        with open(file_path, "rb") as f:
            data = pkl.load(f)

            self.__distance_matrix = data["DistanceMatrix"]
            self.__nodes = data["Nodes"]
            self.__vehicle_capacity = data["VehicleCapacity"]

    def save(self, file_path: str):
        """
            Save this data into a **pickle** file

            :param file_path: The path of the file
        """
        with open(file_path, "wb") as f:
            pkl.dump({
                "DistanceMatrix": self.__distance_matrix,
                "Nodes": self.__nodes,
                "VehicleCapacity": self.__vehicle_capacity
            }, f)

    @staticmethod
    def generate_random(number_of_stores: int, vehicle_capacity: float = 50., seed: Optional[int] = 12,
                        distance_mu: float = 30.,
                        distance_std: float = 10.,
                        load_mu: float = 10.,
                        load_std: float = 5.) -> Data:
        """
            This method randomly generate a data based on given parameters.

            :param number_of_stores: The number of stores
            :param vehicle_capacity: The vehicle load capacity
            :param seed: Random seed
            :param distance_mu: The mean value of traveling distance between nodes
            :param distance_std: The standard deviation value of traveling distance between nodes
            :param load_mu: The mean value of load amount for a store node
            :param load_std: The standard deviation value of load amount for a store node
            :return: Randomly generated **Data** object
        """

        # Validity of the given parameters
        assert number_of_stores is not None and number_of_stores > 0, "Invalid number of stores"
        assert vehicle_capacity is not None and vehicle_capacity > 0, "Invalid vehicle load capacity"

        assert distance_mu > 0, "Invalid mean for traveling distance"
        assert distance_std > 0, "Invalid std for traveling distance"
        assert load_mu > 0, "Invalid mean for load amount"
        assert load_std > 0, "Invalid std for load amount"

        # Generate random object
        rnd = Random(seed) if seed is not None else Random()

        # Generate Data object
        data = Data()

        data.__vehicle_capacity = vehicle_capacity

        # Initiate nodes
        data.__nodes = [Node(i, round(min(max(1., rnd.gauss(load_mu, load_std)), vehicle_capacity), 3) if i > 0 else 0.)
                        for i in range(number_of_stores + 1)]

        # Initiate distance matrix
        data.__distance_matrix = {}

        for i in range(number_of_stores + 1):
            data.__distance_matrix[i] = {}

            for j in range(number_of_stores + 1):
                if i == j:
                    data.__distance_matrix[i][j] = 0.
                    continue

                data.__distance_matrix[i][j] = round(max(1., rnd.gauss(distance_mu, distance_std)), 3)

        return data
