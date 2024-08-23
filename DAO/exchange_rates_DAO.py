import sqlite3

from DAO.base_DAO import BaseDAO, ConnectManager
from DTO.exchange_rate_DTO import ExchangeRateCodesDTO, ExchangeRateDetailDTO
from DTO.currency_DTO import CurrencyDTO
from exceptions import ExchangeRateNotFoundError, InsertAlreadyExistsExchangeRateError, CurrenciesNotExistsError


class ExchangeRatesDAO(BaseDAO):
    _QUERIES = {
        'get_all': '''SELECT er.ID, 
                             er.Rate,
                             base.ID,
                             base.Code,
                             base.FullName,
                             base.Sign,
                             target.ID,
                             target.Code,
                             target.FullName,
                             target.Sign
                    FROM ExchangeRates er
                    JOIN Currencies base ON er.BaseCurrencyID = base.ID
                    JOIN Currencies target ON er.TargetCurrencyID = target.ID;''',
        'get_by_codes': '''SELECT er.ID, 
                                  er.Rate,
                                  base.ID,
                                  base.Code,
                                  base.FullName,
                                  base.Sign,
                                  target.ID,
                                  target.Code,
                                  target.FullName,
                                  target.Sign
                FROM ExchangeRates er
                JOIN Currencies base ON er.BaseCurrencyID = base.ID
                JOIN Currencies target ON er.TargetCurrencyID = target.ID
                WHERE base.CODE = ? AND target.CODE = ?''',
        'insert': '''INSERT INTO ExchangeRates (BaseCurrencyID, TargetCurrencyID, Rate)
                SELECT base.ID as BaseCurrencyID, target.ID as TargetCurrencyID, ?
                FROM Currencies as base
                JOIN Currencies as target ON base.Code = ? AND target.Code = ?
                WHERE EXISTS(SELECT TRUE FROM Currencies WHERE Code = ?)
                AND EXISTS(SELECT TRUE FROM Currencies WHERE Code = ?);''',
        'update': '''UPDATE ExchangeRates 
                SET Rate = ? 
                WHERE BaseCurrencyID = (SELECT ID FROM Currencies WHERE Code = ?) AND 
                TargetCurrencyID = (SELECT ID FROM Currencies WHERE Code = ?);''',
        'check_currencies': '''SELECT TRUE FROM Currencies
                               WHERE (SELECT TRUE FROM Currencies WHERE Code = ?)
                               AND (SELECT TRUE FROM Currencies WHERE Code = ?);''',
    }

    def get_all(self):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            return cursor.execute(self._QUERIES['get_all']).fetchall()

    def get_by_codes(self, base_code: str, target_code: str):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            response = cursor.execute(self._QUERIES['get_by_codes'], (base_code, target_code)).fetchone()

        self._validate_response(response, base_code, target_code)
        return response

    def insert(self, dto: ExchangeRateCodesDTO):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            self._check_currencies_availability(
                dto.base_currency_code,
                dto.target_currency_code
            )

            try:
                cursor.execute(
                    self._QUERIES['insert'],
                    (
                        dto.rate,
                        dto.base_currency_code,
                        dto.target_currency_code,
                        dto.base_currency_code,
                        dto.target_currency_code
                    )
                )
            except sqlite3.IntegrityError:
                raise InsertAlreadyExistsExchangeRateError(dto.base_currency_code, dto.target_currency_code)

        return self.get_by_codes(dto.base_currency_code, dto.target_currency_code)

    def update(self, dto: ExchangeRateCodesDTO):
        self.get_by_codes(dto.base_currency_code, dto.target_currency_code)

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                self._QUERIES['update'], (dto.rate, dto.base_currency_code, dto.target_currency_code)
            )

        return self.get_by_codes(dto.base_currency_code, dto.target_currency_code)

    def _check_currencies_availability(self, base_code: str, target_code: str):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            if not cursor.execute(self._QUERIES['check_currencies'], (base_code, target_code)).fetchone():
                raise CurrenciesNotExistsError(base_code, target_code)
            return

    @staticmethod
    def _validate_response(response, base_code: str, target_code: str):
        if not response:
            raise ExchangeRateNotFoundError(base_code=base_code, target_code=target_code)
        return


