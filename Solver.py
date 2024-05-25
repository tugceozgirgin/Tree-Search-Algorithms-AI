from abc import ABC, abstractmethod
from Data import Data, Solution


class Solver(ABC):
    """
        This *abstract* class solves the assignment problem.
    """
    data: Data  #: Target problem data

    def __init__(self, data: Data):
        """
            Constructor

            :param data: Target problem data
        """
        self.data = data

    @abstractmethod
    def solve(self) -> Solution:
        """
            This method solves the given problem data, and returns the solution. Solution is a sequence indicating the
            traveling path.

            :return: Solution as ``Sequence[Node]`` format.
        """
        ...

    @property
    def empty_solution(self) -> Solution:
        """
            This method provides an empty solution.

            :return: Solution with empty path.
        """
        return []
