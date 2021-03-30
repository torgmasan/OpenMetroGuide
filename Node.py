"""This file contains the station class which serves as the vertex
for the OMG graph."""
from __future__ import annotations

from typing import Union


class Node:
    """A class for the vertices of the graph that provide the necessary
    information of a station.

    Instance Attributes:
        - name: The name of the station.
        - destination_distance: Direct distance of the current station to the final station by the
                                method of 'as the crow flies'.
        - final_score: Keeps track of the score of the vertex. Like a rank (lower the better).
        - colors:
        - from_node: Keeps track of the previous node to make connections in the algorithm.
        - neighbouring_station: The Station(vertices) that are adjacent to this station.
        - coordinates: Coordinates of the current station on the grid(graph).

    """

    # Private Instance Attributes:
    #    - _is_station: Whether
    name: str
    destination_distance: float
    final_score: float
    colors: set[str]
    _is_station: bool
    from_node: Union[str, Node]  # Want to keep name or the vertex itself?
    neighbouring_stations: dict[Node, float]  # same as below, not sure whether Track attribute or here.
    coordinates: tuple[float, float]

    def __init__(self, station_name: str, destination_distance: float, final_score: float,
                 previous_node: Union[str, Node], neighbours: set[Node],
                 coordinates: tuple[float, float]) -> None:
        """Initialize a new Station object."""
        self.name = station_name
        self.destination_distance = destination_distance
        self.final_score = final_score
        self.from_node = previous_node
        self.neighbouring_stations = neighbours
        self.coordinates = coordinates

    def degree(self) -> int:
        """Calculates the degree of the current station, i.e., how many other vertices are connected
        to this current vertex."""
        return len(self.neighbouring_stations)

