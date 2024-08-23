from dataclasses import dataclass


@dataclass
class CurrencyDTO:
    code: str
    name: str
    sign: str
    id: int = None


@dataclass
class CurrencyIDDTO:
    id: int
    code: str
    name: str
    sign: str


