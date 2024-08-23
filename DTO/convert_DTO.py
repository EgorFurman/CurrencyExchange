from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ConvertDTO:
    base_currency_code: str
    target_currency_code: str
    amount: Decimal


@dataclass
class ConvertDetailDTO:
    baseCurrency: dict[str: int, str: str, str: str, str: str]
    targetCurrency: dict[str: int, str: str, str: str, str: str]
    rate: Decimal
    amount: Decimal
    convertedAmount: Decimal
