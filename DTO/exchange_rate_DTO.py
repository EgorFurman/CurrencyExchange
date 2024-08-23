from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ExchangeRateCodesDTO:
    base_currency_code: str
    target_currency_code: str
    rate: float = None


@dataclass
class ExchangeRateDetailDTO:
    id: int
    baseCurrency: dict[str: int, str: str, str: str, str: str]
    targetCurrency: dict[str: int, str: str, str: str, str: str]
    rate: Decimal




