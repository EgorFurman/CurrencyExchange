from decimal import Decimal

from controller.base_controller import Controller
from DAO.exchange_rates_DAO import ExchangeRatesDAO
from DTO import ExchangeRateCodesDTO, ExchangeRateDetailDTO, ConvertDTO, CurrencyIDDTO
from service.service import ConvertService
from exceptions import MissingCurrencyCodeError


class ExchangeRatesController(Controller):
    _DAO = ExchangeRatesDAO()
    _NECESSARY_POST_FIELDS = ('baseCurrencyCode', 'targetCurrencyCode', 'rate')
    _NECESSARY_PATCH_FIELDS = ('rate', )
    _NECESSARY_CONVERT_FIELDS = ('from', 'to', 'amount')

    def __init__(self):
        self._SERVICE = ConvertService(self)
        super().__init__()

    def get(self, codes: str = None) -> ExchangeRateDetailDTO | list[ExchangeRateDetailDTO]:
        if codes:
            codes = self._parse_codes(codes)
            return self._to_DTO(self._DAO.get_by_codes(*codes))
        return [self._to_DTO(r) for r in self._DAO.get_all()]

    def insert(self, data: str) -> ExchangeRateDetailDTO:
        parsed_data = self._parse_data(data=data, necessary_fields=self._NECESSARY_POST_FIELDS)
        response = self._DAO.insert(
            ExchangeRateCodesDTO(
                base_currency_code=parsed_data['baseCurrencyCode'],
                target_currency_code=parsed_data['targetCurrencyCode'],
                rate=round(float(parsed_data['rate']), 6),
            )
        )

        return self._to_DTO(response)

    def update(self, codes: str, data: str) -> ExchangeRateDetailDTO:
        parsed_data = self._parse_data(data, necessary_fields=self._NECESSARY_PATCH_FIELDS)
        codes = self._parse_codes(codes)

        response = self._DAO.update(
            ExchangeRateCodesDTO(
                *codes,
                rate=round(float(parsed_data['rate']), 6)
            )
        )

        return self._to_DTO(response)

    def delete(self, *args, **kwargs):
        ...

    def convert(self, data: str):
        parsed_data = self._parse_data(data, necessary_fields=self._NECESSARY_CONVERT_FIELDS)
        response = self._SERVICE.convert(
            ConvertDTO(
                base_currency_code=parsed_data['from'],
                target_currency_code=parsed_data['to'],
                amount=Decimal(parsed_data['amount']).quantize(Decimal('0.01'))
            )
        )
        return response

    @staticmethod
    def _parse_codes(codes: str):
        try:
            return codes[:3], codes[3:]
        except Exception:
            raise MissingCurrencyCodeError

    @staticmethod
    def _to_DTO(response):
        return ExchangeRateDetailDTO(
            id=response[0],
            baseCurrency=CurrencyIDDTO(*response[2:6]).__dict__,
            targetCurrency=CurrencyIDDTO(*response[6:]).__dict__,
            rate=Decimal(response[1]).quantize(Decimal('0.01'))
        )



