from __future__ import annotations
from typing import Union


class Node:
    """
        This class represents a **Node**
    """

    __node_id: int     #: Each node has a unique id
    __is_depot: bool   #: Whether this node is a depot, or a store
    __load: float      #: Load amount of a store node

    def __init__(self, node_id: int, load: float = 0):
        self.__node_id = node_id
        self.__is_depot = node_id == 0

        if self.is_store:
            self.__load = load
        else:
            self.__load = 0

    @property
    def id(self) -> int:
        """
            This method provides the id of the node

            :return: Node ID
        """
        return self.__node_id

    @property
    def is_depot(self) -> bool:
        """
            This method provides whether the node is a *depot* node, or a *store* node

            :return: If the node is a *depot* node
        """

        return self.__is_depot

    @property
    def is_store(self) -> bool:
        """
            This method provides whether the node is a *store* node, or a *depot* node

            :return: If the node is a *store* node
        """

        return not self.__is_depot

    @property
    def load(self) -> float:
        """
            This method provides the load amount of the *store* node

            :return: Load amount
        """
        return self.__load

    def __eq__(self, other: Union[Node, int]) -> bool:
        """
            Equality check based on Node ID

            :param other: Comparing object
            :return: Whether these agents are equal.
        """
        if isinstance(other, Node):
            return self.__node_id == other.__node_id
        elif isinstance(other, int):
            return self.__node_id == other
        else:
            return False

    def __hash__(self):
        """
            Hashing based on Node ID

            :return: Hash value of the node
        """
        return self.__node_id
