"""Represent the transit map in the form of a graph.
"""
from __future__ import annotations

from typing import Optional, Any

from Node import Node
import math
from dataclasses import dataclass


@dataclass
class QueueElement:
    """A member of the PriorityQueue created when
    finding the optimized route.
    """
    name: str
    score_from_start: float
    distance_to_destination: float
    total_score: float
    previous_vertex: Optional[QueueElement] = None


def get_path(curr_element: QueueElement) -> list[str]:
    """Return a list of nodes corresponding to the shortest
    path from start to destination.
    """
    if curr_element.previous_vertex is None:
        return [curr_element.name]
    else:
        return get_path(curr_element.previous_vertex) + [curr_element.name]


def get_element(node_queue: list[QueueElement], name: str) -> Optional[QueueElement]:
    """Return the element with name in the priority queue.
    """
    for element in node_queue:
        if element.name == name:
            return element


def update_element(node_queue: list[QueueElement], name: str, new_score_from_start: float,
                   new_previous: QueueElement) -> None:
    """Updates the distance between start and element with name if
    new_distance_from_start is less than the previous distance from start.

    Also update the previous node.
    """
    element = get_element(node_queue, name)
    new_total_score = new_score_from_start + element.distance_to_destination

    if element.total_score > new_total_score:
        element.total_score = new_total_score
        element.score_from_start = new_score_from_start
        element.previous_vertex = new_previous


def sort_queue(node_queue: list[QueueElement]) -> None:
    """Sort the priority queue in increasing order of QueueElement.total_score.
    """
    node_queue.sort(key=lambda x: x.total_score)


def dequeue(node_queue: list[QueueElement]) -> QueueElement:
    """Remove and return the first element from the priority queue.
    """
    return node_queue.pop(0)


class Map:
    """Represent the graph of the map where the calculation
    to find the shortest/cheapest route will take place.
    """
    # Instance Attributes:
    #   - _nodes: A collection of nodes in this Map.

    _nodes: dict[str, Node]

    def __init__(self) -> None:
        """Initialize an empty transit(metro) map
        without any stations or tracks.
        """
        self._nodes = {}

    def get_node(self, name: str) -> Node:
        """Return corresponding node of input name.
        If no name found, raise ValueError.
        """
        if name in self._nodes:
            return self._nodes[name]
        else:
            raise ValueError

    def get_all_nodes(self, kind: str = '') -> set[Node]:
        """Return a set of all nodes in the map.

        Preconditions:
            - kind in {'', 'station', 'corner'}
        """
        all_nodes = set(self._nodes.values())
        if kind == '':
            return all_nodes
        elif kind == 'station':
            return {node for node in all_nodes if node.is_station}
        else:
            return {node for node in all_nodes if not node.is_station}

    def add_node(self, node: Node) -> None:
        """Add a node to the map.
        """
        self._nodes[node.name] = node

    def add_track(self, name_1: str, name_2: str, color: str) -> None:
        """Add a weighted track to the map.
        If any are absent, raise ValueError.
        """
        if name_1 and name_2 in self._nodes:
            node_1 = self._nodes[name_1]
            node_2 = self._nodes[name_2]
            node_1.add_track(node_2, color)
        else:
            raise ValueError

    def get_track_weight(self, name_1: str, name_2: str, optimization: str) -> float:
        """Return the weight of the track between two nodes.

        Raise ValueError if no such track exists.

        Preconditions:
            optimization in {'distance', 'cost'}
        """
        if name_1 and name_2 in self._nodes:
            node_1 = self._nodes[name_1]
            node_2 = self._nodes[name_2]

            neighboring_stations = node_1.get_neighbours()

            if node_2 in neighboring_stations:
                wt = node_1.get_weight(node_2, optimization)
                return wt

        raise ValueError

    def optimized_route(self, start: str, destination: str,
                        optimization: str = 'distance') -> list[str]:
        """Return the most optimized route using the Dijkstra Algorithm.
        Runs the optimization depending on what the option entered is.

        Preconditions:
            optimization in {'distance', 'cost'}
        """
        start_node = self.get_node(start)
        end_node = self.get_node(destination)
        node_queue = [QueueElement(start, 0,
                                   start_node.get_distance(end_node),
                                   start_node.get_distance(end_node))]
        node_queue.extend([QueueElement(name, math.inf,
                                        self._nodes[name].get_distance(end_node), math.inf)
                           for name in self._nodes if name != start])

        while (curr_element := dequeue(node_queue)).name != destination:
            tmp_node = self._nodes[curr_element.name]

            for node in tmp_node.get_neighbours():
                to_add = self.get_track_weight(tmp_node.name, node.name, optimization)

                if get_element(node_queue, node.name) is not None:
                    update_element(node_queue, node.name,
                                   to_add + curr_element.score_from_start, curr_element)
                sort_queue(node_queue)

        return get_path(curr_element)
