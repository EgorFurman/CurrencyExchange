import sqlite3
from core.config import settings


QUERIES = {
    'init_currencies': '''CREATE TABLE IF NOT EXISTS Currencies (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Code Varchar(3) NOT NULL UNIQUE,
                FullName Varchar(30) NOT NULL,
                Sign Varchar(5))''',
    'init_exchange_rates': '''CREATE TABLE IF NOT EXISTS ExchangeRates (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                BaseCurrencyID INTEGER,
                TargetCurrencyID INTEGER,
                Rate Decimal(6, 4),
                FOREIGN KEY (BaseCurrencyID) REFERENCES Currencies (ID),
                FOREIGN KEY (TargetCurrencyID) REFERENCES Currencies (ID))''',
    'init_exchange_rates_index': '''CREATE UNIQUE INDEX IF NOT EXISTS unique_pair 
                ON ExchangeRates(BaseCurrencyID, TargetCurrencyID)'''
}


def init_db():
    with sqlite3.connect(settings.db_name) as connection:
        cursor = connection.cursor()
        cursor.execute(QUERIES['init_currencies'])
        cursor.execute(QUERIES['init_exchange_rates'])
        cursor.execute(QUERIES['init_exchange_rates_index'])


if __name__ == '__main__':
    init_db()



