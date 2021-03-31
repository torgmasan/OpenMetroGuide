"""This file contains the station class which serves as the vertex
for the OpenMetroGuide graph."""
from __future__ import annotations


class _Node:
    """A class for the vertices of the graph that provide the necessary
    information of a station or a corner.

    Instance Attributes:
        - name: The name of the station.
        - colors: Represents the color line of the current node.
        - neighbouring_station: The Station(vertices) that are adjacent to this station.
        - coordinates: Coordinates of the current station on the grid(graph).

    """

    # Private Instance Attributes:
    #    - _is_station: Whether node is station or corner
    colors: set[str]
    _is_station: bool
    neighbouring_stations: dict[_Node, tuple[float, float]]
    coordinates: tuple[float, float]

    def __init__(self, colors: set[str],
                 neighbouring_stations: dict[_Node, tuple[float, float]],
                 coordinates: tuple[float, float], _is_station: bool) -> None:
        """Initialize a new Station object."""
        self.neighbouring_stations = neighbouring_stations
        self.colors = colors
        self.coordinates = coordinates
        self._is_station = _is_station

    def degree(self) -> int:
        """Calculates the degree of the current station, i.e., how many other vertices are connected
        to this current vertex."""
        return len(self.neighbouring_stations)

    def is_station(self) -> bool:
        """Returns if current node is a station or not"""
        return self._is_station
