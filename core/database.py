import sqlite3
from contextlib import contextmanager

from exceptions import DatabaseAccessError


class ConnectManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        connection = sqlite3.connect(self.db_path)
        try:
            yield connection
        except Exception as e:
            print(e)
            raise DatabaseAccessError(e)
        finally:
            connection.close()

    @contextmanager
    def get_cursor(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            try:
                yield cursor
                connection.commit()
            finally:
                cursor.close()
