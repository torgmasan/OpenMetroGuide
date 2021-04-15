"""This file is the manager of the links to the database of
OpenMetroGuide (currently local database). It will handle reading and writing
to be used by all pygame windows that interact with stored Metro lines.
"""
import sqlite3
from Map import Map

conn = sqlite3.connect('map_storage.db')
cursor = conn.cursor()


def init_db() -> None:
    """Initializes the database with tables as required."""
    with conn:
        station_cmd = """CREATE TABLE IF NOT EXISTS
        stations(city TEXT, name TEXT, is_station TEXT, x INT, y INT, ZONE INT, 
        PRIMARY KEY(city, name))"""

        cursor.execute(station_cmd)

        connection_cmd = """CREATE TABLE IF NOT EXISTS
        connections(city TEXT, name_1 TEXT, name_2 TEXT, FOREIGN KEY(city, name_1)
        REFERENCES stations(city, name_1) FOREIGN KEY(city, name_2) REFERENCES
        stations(city, name_2))"""

        cursor.execute(connection_cmd)


if __name__ == "__main__":
    init_db()
    conn.close()
