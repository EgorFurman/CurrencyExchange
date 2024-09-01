import sqlite3
from core.config import settings

QUERIES_TO_CURRENCIES = {
    'create_USD': 'INSERT INTO Currencies (Code, FullName, Sign) VALUES ("USD", "US Dollar", "$")',
    'create_EUR': 'INSERT INTO Currencies (Code, FullName, Sign) VALUES ("EUR", "Euro", "€")',
    'create_RUB': 'INSERT INTO Currencies (Code, FullName, Sign) VALUES ("RUB", "Russian Ruble", "₽")'
}

QUERIES_TO_EXCHANGE_RATES = {
    'create_USD_to_RUB': 'INSERT INTO ExchangeRates (BaseCurrencyID, TargetCurrencyID, Rate) VALUES (1, 2, 0.92)',
    'create_USD_to_EUR': 'INSERT INTO ExchangeRates (BaseCurrencyID, TargetCurrencyID, Rate) VALUES (1, 3, 91.43)',
}


def fill_db() -> None:
    with sqlite3.connect(settings.db_name) as connection:
        cur = connection.cursor()

        for query in QUERIES_TO_CURRENCIES.values():
            cur.execute(query)

        for query in QUERIES_TO_EXCHANGE_RATES.values():
            cur.execute(query)


if __name__ == '__main__':
    fill_db()