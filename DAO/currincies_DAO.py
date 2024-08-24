import sqlite3

from DAO.base_DAO import BaseDAO
from DTO.currency_DTO import CurrencyDTO
from exceptions import CurrencyNotFoundError, InsertAlreadyExistsCurrencyError


class CurrenciesDAO(BaseDAO):
    _QUERIES = {
        'get_all': 'SELECT * FROM Currencies',
        'get_by_id': 'SELECT * FROM Currencies WHERE ID = ?',
        'get_by_code': 'SELECT * FROM Currencies WHERE Code = ?',
        'insert': 'INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)',
    }

    def get_all(self):
        with sqlite3.connect(self._DB_PATH) as connection:
            cursor = connection.cursor()

            return cursor.execute(self._QUERIES['get_all']).fetchall()

    def get_by_id(self, id) -> list[tuple[int, str, str, str]]:
        with sqlite3.connect(self._DB_PATH) as connection:
            cursor = connection.cursor()

            response = cursor.execute(self._QUERIES['get_by_id'], (id,)).fetchone()

        self._validate_response(response, column='id', value=id)
        return response

    def get_by_code(self, code: str) -> tuple[int, str, str, str]:
        with sqlite3.connect(self._DB_PATH) as connection:
            cursor = connection.cursor()
            response = cursor.execute(self._QUERIES['get_by_code'], (code,)).fetchone()

        self._validate_response(response, column='code', value=code)
        return response

    def insert(self, dto: CurrencyDTO) -> tuple[int, str, str, str]:
        with sqlite3.connect(self._DB_PATH) as connection:
            cursor = connection.cursor()

            try:
                cursor.execute(self._QUERIES['insert'], (dto.code, dto.name, dto.sign))
            except sqlite3.IntegrityError:
                raise InsertAlreadyExistsCurrencyError(dto.code)

        return self.get_by_code(dto.code)

    @staticmethod
    def _validate_response(response, column, value):
        if not response:
            raise CurrencyNotFoundError(column, value)
        return






