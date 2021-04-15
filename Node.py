"""This file contains the station class which serves as the vertex
for the OpenMetroGuide graph."""
from __future__ import annotations

import math
from typing import Any, Optional


class Node:
    """A class for the vertices of the graph that provide the necessary
    information of a station or a corner.

    Instance Attributes:
        - name: The name of the station.
        - colors: Represents the color line of the current node.
        - is_station: Whether the current node is a station or a corner.
        - coordinates: Coordinates of the current station on the grid(graph).

    Representation Invariants:
        - self not in self._neighbouring_nodes
        - all(self in u._neighbouring_nodes for u in self._neighbouring_nodes)

    """

    # Private Instance Attributes:
    #    - _neighbouring_nodes: The nodes which are adjacent to the current node
    #    and their corresponding weights with the current node.
    name: str
    # colors: set[str]
    is_station: bool
    _neighbouring_nodes: dict[Node, tuple[float, int, str]]
    coordinates: tuple[int, int]
    zone: Any

    def __init__(self, name: str,
                 coordinates: tuple[int, int], is_station: bool, zone: Any) -> None:
        """Initialize a new Station object."""
        self.name = name
        self._neighbouring_nodes = {}
        # self.colors = colors
        self.coordinates = coordinates
        self.is_station = is_station
        self.zone = zone

    def add_track(self, node_2: Node, color: str) -> None:
        """Add track between this node and node_2 with color"""
        weight_1 = self.get_distance(node_2)
        weight_2 = self.count_zones(node_2)
        self._neighbouring_nodes[node_2] = weight_1, weight_2, color
        node_2._neighbouring_nodes[self] = weight_1, weight_2, color

    def remove_track(self, node_2: Node) -> None:
        """Remove track between this node and node_2

        Preconditions:
            - self.is_adjacent(node_2)
        """
        self._neighbouring_nodes.pop(node_2)
        node_2._neighbouring_nodes.pop(self)

    def is_adjacent(self, node_2: Node) -> bool:
        """Return whether this node and node_2 are neighbours"""
        return self in node_2._neighbouring_nodes and node_2 in self._neighbouring_nodes

    def check_connected(self, node_2: Node, visited: set[Node]) -> bool:
        """Return whether this node is connected to node_2,
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited
        """
        if self.name == node_2.name:
            visited.add(self)
            return True
        else:
            visited.add(self)
            for u in self._neighbouring_nodes:
                if u not in visited:
                    if u.check_connected(node_2, visited):
                        return True
            return False

    def get_closest_station(self, visited: set[Node]) -> Optional[Node]:
        """Return the closest station to this node
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited
        """
        if self.is_station:
            return self
        else:
            visited.add(self)
            for u in self._neighbouring_nodes:
                if u not in visited:
                    return u.get_closest_station(visited)
            return None

    def get_color(self, node_2: Node) -> str:
        """Return the color of the track between this node and node_2

        Preconditions:
            - self.is_adjacent(node_2)
        """
        return self._neighbouring_nodes[node_2][2]

    def get_neighbours(self, kind: str = '') -> set[Node]:
        """Return the neighboring nodes of this node, according to the kind of
        node requested by the user.

        Preconditions:
            - kind in {'', 'station', 'corner'}
        """
        all_neighbours = set(self._neighbouring_nodes.keys())
        if kind == '':
            return all_neighbours
        elif kind == 'station':
            return {node for node in all_neighbours if node.is_station}
        else:
            return {node for node in all_neighbours if not node.is_station}

    def get_weight(self, node2: Node, optimization: str) -> float:
        """Returns the weight between two nodes. This weight could
        be either in terms of the distance or the cost unit between the nodes.

        Preconditions:
            - optimization in {'distance', 'cost'}
        """
        if optimization == 'distance':
            return self._neighbouring_nodes[node2][0]
        else:
            return self._neighbouring_nodes[node2][1]

    def get_distance(self, destination_node: Node) -> float:
        """Returns the direct distance from the
        current node to the destination node.
        """
        x1, x2 = self.coordinates[0], destination_node.coordinates[0]
        y1, y2 = self.coordinates[1], destination_node.coordinates[1]
        weight = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return weight

    def count_zones(self, destination_node: Node) -> int:
        """Returns the cost in terms of base units (where a base unit
        is the price from two nodes in the same zone)."""
        if self.zone == destination_node.zone or self.zone == ''\
                or destination_node.zone == '':
            return 1
        else:
            return 2
