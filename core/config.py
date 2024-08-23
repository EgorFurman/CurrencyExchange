from pathlib import Path
from dataclasses import dataclass


@dataclass
class Settings:
    db_name = 'CurrencyExchange.db'
    db_path = rf'{Path.cwd()}\db\CurrencyExchange.db'


settings = Settings()

