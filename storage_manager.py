"""This file is the manager of the links to the database of
OpenMetroGuide (currently local database). It will handle reading and writing
to be used by all pygame windows that interact with stored Metro lines.
"""
import sqlite3
from Map import Map
from Node import Node

conn = sqlite3.connect('map_storage.db')
cursor = conn.cursor()


def init_db() -> None:
    """Initializes the database with tables as required."""
    with conn:
        station_cmd = """CREATE TABLE IF NOT EXISTS
        nodes(city TEXT, name TEXT, is_station TEXT, x INT, y INT, zone INT)"""

        cursor.execute(station_cmd)

        connection_cmd = """CREATE TABLE IF NOT EXISTS
        connections(city TEXT, name_1 TEXT, name_2 TEXT)"""

        cursor.execute(connection_cmd)


def store_map(city: str, active_nodes: set) -> None:
    """Takes in the current active nodes in the metro map of provided city
    and stores it in the local database.

    Preconditions:
        - Used by Admin only.
    """
    init_db()
    active_rows = create_rows_stations(city, active_nodes)
    with conn:
        cursor.execute("SELECT * FROM nodes WHERE city=?", (city, ))
        curr_rows = set(cursor.fetchall())
        to_add = active_rows.difference(curr_rows)
        to_remove = curr_rows.difference(active_rows)
        to_update = curr_rows.intersection(active_rows)

        for element in to_add:
            cursor.execute("""INSERT INTO nodes VALUES (:city, :name, :is_station, :x, :y, :zone)""",
                           {'city': element[0], 'name': element[1], 'is_station': element[2], 'x': element[3],
                            'y': element[4], 'zone': element[5]})


def create_rows_stations(city: str, active_nodes: set[Node]) -> set[tuple[str, str, str, int, int, int]]:
    """Creates row entries from the active nodes provided"""
    row_set = set()
    for node in active_nodes:
        row_set.add((city, node.name, str(node.is_station), node.coordinates[0],
                     node.coordinates[1], node.zone))

    return row_set


def get_map(city: str) -> Map:
    """Takes in the city as input and gets the corresponding map
    that is currently stored in the database

    Preconditions:
        - city exists in the local database
    """
    init_db()
    metro_map = Map()

    with conn:
        pass

    return metro_map


if __name__ == "__main__":
    init_db()
    store_map('', {Node('A', (40, 40), True, '1')})
    conn.close()
