from Node import Node


class Map:
    """Represents the graph of the map where the calculation to find the shortest/cheapest route
    will take place.
    """
    # Instance Attributes:
    #   - _stations: A collection of stations in this Map. Maps station name to Station instance.
    #   - _tracks: A collection of tracks in this Map. ...

    _stations: dict[str, Node]
    _tracks: ...

    def __init__(self) -> None:
        """Initializes an empty transit(metro) map without any stations or tracks."""
        self._stations = {}
        self._tracks = ...