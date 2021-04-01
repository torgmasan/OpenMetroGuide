from __future__ import annotations

from typing import Optional

from Node import _Node
import math
from dataclasses import dataclass


@dataclass
class QueueElement:
    """A member of the PriorityQueue created when
    finding the optimized route.
    """
    name: str
    distance_from_start: float
    previous_vertex: Optional[QueueElement] = None


def get_path(curr_element: QueueElement) -> list[str]:
    if curr_element.previous_vertex is None:
        return [curr_element.name]
    else:
        return get_path(curr_element.previous_vertex) + [curr_element.name]


def get_element(node_queue: list[QueueElement], name: str) -> QueueElement:
    for element in node_queue:
        if element.name == name:
            return element


def update_element(node_queue: list[QueueElement], name: str,
                   new_distance_from_start: int) -> None:
    get_element(node_queue, name).distance_from_start = new_distance_from_start


def enqueue(node_queue: list[QueueElement], entry: QueueElement) -> None:
    node_queue.remove(entry)

    for i in range(0, len(node_queue) - 1):
        if entry.distance_from_start < node_queue[i].distance_from_start:
            node_queue.insert(i, entry)


def dequeue(node_queue: list[QueueElement]) -> QueueElement:
    return node_queue.pop(0)


class Map:
    """Represents the graph of the map where the calculation to find the shortest/cheapest route
    will take place.
    """
    # Instance Attributes:
    #   - _stations: A collection of stations in this Map. Maps station name to Station instance.
    #   - _tracks: A collection of tracks in this Map. ...

    _nodes: dict[str, _Node]

    def __init__(self) -> None:
        """Initializes an empty transit(metro) map without any stations or tracks."""
        self._nodes = {}

    def get_node(self, name: str) -> _Node:
        """Returns corresponding node of input name
        If no name found, raise ValueError
        """
        if name in self._nodes:
            return self._nodes[name]
        else:
            raise ValueError

    def add_node(self, name: str, colors: set[str],
                 coordinates: tuple[float, float], is_station: bool) -> None:
        """Adds a node to the map"""
        self._nodes[name] = _Node(name, colors, coordinates, is_station)

    def add_track(self, name_1: str, name_2: str) -> None:
        """Adds a weighted track to the map
        If any are absent, raise ValueError
        """
        if name_1 and name_2 in self._nodes:
            node_1 = self._nodes[name_1]
            node_2 = self._nodes[name_2]
            node_1.add_track(node_2)
        else:
            raise ValueError

    def get_track_weight(self, name_1: str, name_2: str) -> float:
        """Returns the weight of the track between two nodes.
        Raises ValueError if no such track exists
        """
        if name_1 and name_2 in self._nodes:
            node_1 = self._nodes[name_1]
            node_2 = self._nodes[name_2]

            neighboring_stations = node_1.get_neighbours()

            if node_2 in neighboring_stations:
                wt = node_1.get_weight(node_2)
                return wt

        raise ValueError

    def optimized_route(self, start: str, destination: str) -> list[str]:
        """Returns the most optimized route """
        node_queue = [QueueElement(start, 0)]
        node_queue.extend([QueueElement(name, math.inf) for name in self._nodes
                           if name != start])

        while (curr_element := dequeue(node_queue)).name != destination:
            tmp_node = self._nodes[curr_element.name]

            for node in tmp_node.get_neighbours():
                to_add = tmp_node.get_weight(node)

                new_element = get_element(node_queue, node.name)

                new_element.distance_from_start = to_add + curr_element.distance_from_start
                enqueue(node_queue, new_element)

        return get_path(curr_element)


if __name__ == "__main__":
    m = Map()
    for ch in 'ABCDE':
        m.add_node(ch, set(), (0, 0), True)

    m.add_track('A', 'D')
    m.add_track('A', 'B')
    m.add_track('D', 'B')
    m.add_track('D', 'E')
    m.add_track('E', 'B')
    m.add_track('E', 'C')
    m.add_track('B', 'C')

    m.get_node('A'). _neighbouring_nodes[m.get_node('D')] = 1
    m.get_node('A')._neighbouring_nodes[m.get_node('B')] = 6
    m.get_node('D')._neighbouring_nodes[m.get_node('B')] = 2
    m.get_node('D')._neighbouring_nodes[m.get_node('E')] = 1
    m.get_node('E')._neighbouring_nodes[m.get_node('B')] = 2
    m.get_node('E')._neighbouring_nodes[m.get_node('C')] = 5
    m.get_node('B')._neighbouring_nodes[m.get_node('C')] = 5
