from abc import ABC, abstractmethod
from core.config import Settings, settings
from core.database import ConnectManager
import sqlite3


class BaseDAO(ABC):
    def __init__(self):
        self.db_path = '../db/CurrencyExchange.db'

    @abstractmethod
    def _QUERIES(self):
        pass


#with sqlite3.connect('../db/CurrencyExchange.db') as conn:
#    cur = conn.cursor()
#    cur.execute('''UPDATE ExchangeRates
#                SET Rate = 0.1
#                WHERE BaseCurrencyID = (SELECT ID FROM Currencies WHERE Code = "RUB") AND
#                TargetCurrencyID = (SELECT ID FROM Currencies WHERE Code = "USD");''')
#
#    print(cur.fetchone())



