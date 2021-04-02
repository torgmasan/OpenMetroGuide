"""This file contains the station class which serves as the vertex
for the OpenMetroGuide graph."""
from __future__ import annotations

import math


class _Node:
    """A class for the vertices of the graph that provide the necessary
    information of a station or a corner.

    Instance Attributes:
        - name: The name of the station.
        - colors: Represents the color line of the current node.
        - is_station: Whether the current node is a station or a corner.
        - coordinates: Coordinates of the current station on the grid(graph).

    """

    # Private Instance Attributes:
    #    - _neighbouring_nodes: The nodes which are adjacent to the current node
    #    and their corresponding weights with the current node.
    name: str
    colors: set[str]
    is_station: bool
    _neighbouring_nodes: dict[_Node, float]
    coordinates: tuple[float, float]

    def __init__(self, name: str, colors: set[str],
                 coordinates: tuple[float, float], is_station: bool) -> None:
        """Initialize a new Station object."""
        self.name = name
        self._neighbouring_nodes = {}
        self.colors = colors
        self.coordinates = coordinates
        self.is_station = is_station

    def add_track(self, node_2: _Node):
        """Adds track between two nodes"""
        weight = self.get_distance(node_2)
        self._neighbouring_nodes[node_2] = weight
        node_2._neighbouring_nodes[self] = weight

    def get_neighbours(self) -> set[_Node]:
        """Gets the neighboring nodes of the station,
        according to the type of node requested by user.
        """
        return set(self._neighbouring_nodes.keys())

    def get_weight(self, node2: _Node) -> float:
        """Returns the weight between two nodes"""
        return self._neighbouring_nodes[node2]

    def get_distance(self, destination_node: _Node) -> float:
        """Returns the direct distance from the
        current node to the destination node.
        """
        x1, x2 = self.coordinates[0], destination_node.coordinates[0]
        y1, y2 = self.coordinates[1], destination_node.coordinates[1]
        weight = math.sqrt((x2 - x1) ** 2 - (y2 - y1) ** 2)
        return weight
