"""This file is the manager of the links to the database of
OpenMetroGuide (currently local database). It will handle reading and writing
to be used by all pygame windows that interact with stored Metro lines.
"""
import sqlite3
from map import Map
from node import Node


def init_db() -> None:
    """Initializes the database with tables as required."""
    conn = sqlite3.connect('map_storage.db')
    cursor = conn.cursor()

    with conn:
        station_cmd = """CREATE TABLE IF NOT EXISTS
        nodes(city TEXT, name TEXT, is_station TEXT, x INT, y INT, zone TEXT)"""

        cursor.execute(station_cmd)

        connection_cmd = """CREATE TABLE IF NOT EXISTS
        connections(city TEXT, name_1 TEXT, name_2 TEXT, color TEXT)"""

        cursor.execute(connection_cmd)


def store_map(city: str, active_nodes: set) -> None:
    """Takes in the current active nodes in the metro map of provided city
    and stores it in the local database.

    Preconditions:
        - Used by Admin only.
    """
    conn = sqlite3.connect('map_storage.db')
    cursor = conn.cursor()

    active_rows = create_rows_stations(city, active_nodes)
    with conn:
        cursor.execute("SELECT * FROM nodes WHERE city=?", (city,))
        curr_rows = set(cursor.fetchall())
        to_add = {element for element in active_rows if not nodes_row_similar(curr_rows, element)}
        to_remove = {element for element in curr_rows if
                     not nodes_row_similar(active_rows, element)}
        to_update = {element for element in active_rows if nodes_row_similar(curr_rows, element)}

        for element in to_add:
            cursor.execute(
                """INSERT INTO nodes VALUES (:city, :name, :is_station, :x, :y, :zone)""",
                {'city': element[0], 'name': element[1], 'is_station': element[2],
                 'x': element[3], 'y': element[4], 'zone': element[5]})

        for element in to_remove:
            cursor.execute("DELETE FROM nodes WHERE city=? AND name=?", (city, element[1]))

        for element in to_update:
            cursor.execute(
                """UPDATE nodes SET is_station=?, x=?, y=?, zone=? WHERE city=? AND name=?""",
                (element[2], element[3], element[4], element[5], city, element[1]))

        cursor.execute("DELETE FROM connections WHERE city=?", (city,))
        active_connections = create_connection_stations(city, active_nodes)

        for element in active_connections:
            cursor.execute("""INSERT INTO connections VALUES (:city, :name_1, :name_2, :colors)""",
                           {'city': element[0], 'name_1': element[1], 'name_2': element[2],
                            'colors': element[3]})


def nodes_row_similar(all_rows: set[tuple[str, str, str, int, int, int]],
                      identifier: tuple[str, str, str, int, int, int]) -> bool:
    """Returns whether the identifier exists in the input rows.
    """
    for row in all_rows:
        if row[0] == identifier[0] and row[1] == identifier[1]:
            return True
    return False


def create_rows_stations(city: str, active_nodes: set[Node]) -> \
        set[tuple[str, str, str, int, int, int]]:
    """Creates row entries of stations table from the active nodes provided"""
    row_set = set()
    for node in active_nodes:
        row_set.add((city, node.name, str(node.is_station), node.coordinates[0],
                     node.coordinates[1], node.zone))

    return row_set


def create_connection_stations(city: str, active_nodes: set[Node]) -> \
        set[tuple[str, str, str, str]]:
    """Creates row entries of connections from the active nodes provided"""
    row_set = set()
    for node in active_nodes:
        for neighbor in node.get_neighbours():
            row_set.add((city, node.name, neighbor.name, node.get_color(neighbor)))

    return row_set


def get_map(city: str) -> Map:
    """Takes in the city as input and gets the corresponding map
    that is currently stored in the database

    Preconditions:
        - city exists in the local database
    """
    conn = sqlite3.connect('map_storage.db')
    cursor = conn.cursor()
    metro_map = Map()

    with conn:
        cursor.execute("SELECT * FROM nodes WHERE city=?", (city,))
        node_info_lst = cursor.fetchall()

        cursor.execute("SELECT * FROM connections WHERE city=?", (city,))
        connection_info_lst = cursor.fetchall()

        for node_info in node_info_lst:
            is_station = True if node_info[2] == 'True' else False
            metro_map.add_node(Node(node_info[1], (node_info[3], node_info[4]), is_station,
                                    str(node_info[5])))

        for connection_info in connection_info_lst:
            metro_map.add_track(connection_info[1], connection_info[2], connection_info[3])

    return metro_map


def get_cities() -> list[str]:
    """Get all the possible city options in the current local database"""
    conn = sqlite3.connect('map_storage.db')
    cursor = conn.cursor()
    ret_set = set()

    with conn:
        cursor.execute("SELECT city FROM nodes")

        for element in cursor.fetchall():
            ret_set.add(element[0])

    return list(ret_set)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E9969', 'E9988'],
        'extra-imports': ['sqlite3', 'map', 'node'],
        'max-nested-blocks': 4
    })
