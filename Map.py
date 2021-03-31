from Node import _Node


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
                 neighbouring_stations: dict[_Node, tuple[float, float]],
                 coordinates: tuple[float, float], is_station: bool) -> None:
        """Adds a node to the map"""
        self._nodes[name] = _Node(colors, neighbouring_stations,
                                  coordinates, is_station)

    def add_track(self, name_1: str, name_2: str, weight: tuple[float, float]) -> None:
        """Adds a weighted track to the map
        If any are absent, raise ValueError
        """
        if name_1 and name_2 in self._nodes:
            node_1 = self._nodes[name_1]
            node_2 = self._nodes[name_2]
            node_1.neighbouring_stations[node_2] = weight
            node_2.neighbouring_stations[node_1] = weight
        else:
            raise ValueError

    def get_track_weight(self, name_1: str, name_2: str, choice: str = 'distance') -> float:
        """Returns the weight of the track between two nodes.
        Raises ValueError if no such track exists
        """
        if name_1 and name_2 in self._nodes:
            node_1 = self._nodes[name_1]
            node_2 = self._nodes[name_2]

            if node_2 in node_1.neighbouring_stations:
                wt = node_1.neighbouring_stations[node_2]
                if choice == 'distance':
                    return wt[0]
                else:
                    return wt[1]

        raise ValueError

    def optimized_route(self, start: str, destination: str) -> list[str]:
        """Returns the most optimized route """
