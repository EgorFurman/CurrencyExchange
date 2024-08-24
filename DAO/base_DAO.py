from abc import ABC, abstractmethod
from core.config import settings
import sqlite3


class BaseDAO(ABC):
    _DB_PATH = f'./db/{settings.db_name}'

    @abstractmethod
    def _QUERIES(self):
        pass

