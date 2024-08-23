from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller.exchange_rates_controller import ExchangeRatesController

from DTO import ConvertDTO, ConvertDetailDTO
from exceptions import ExchangeRateNotFoundError, ImpossibleConvertError
from controller.currencies_controller import CurrenciesController

class ConvertService:
    def __init__(self, exchange_rates_controller: 'ExchangeRatesController'):
        self._controller = exchange_rates_controller

    def convert(self, convert_dto: ConvertDTO):
        try:
            return self._try_get_direct_convert(convert_dto)
        except ExchangeRateNotFoundError:
            try:
                return self._try_get_inverse_convert(convert_dto)
            except ExchangeRateNotFoundError:
                try:
                    return self._try_get_usd_base_convert(convert_dto)
                except ExchangeRateNotFoundError:
                    raise ImpossibleConvertError(convert_dto.base_currency_code, convert_dto.target_currency_code)

    def _try_get_direct_convert(self, convert_dto: ConvertDTO):
        if convert_dto.base_currency_code == convert_dto.target_currency_code:
            return ConvertDetailDTO(
                baseCurrency=CurrenciesController().get(convert_dto.base_currency_code).__dict__,
                targetCurrency=CurrenciesController().get(convert_dto.target_currency_code).__dict__,
                rate=Decimal(1.00).quantize(Decimal('0.01')),
                amount=convert_dto.amount.quantize(Decimal('0.01')),
                convertedAmount=convert_dto.amount.quantize(Decimal('0.01'))
            )

        direct_rate = self._controller.get(f'{convert_dto.base_currency_code}{convert_dto.target_currency_code}')

        rate = direct_rate.rate

        return ConvertDetailDTO(
            baseCurrency=direct_rate.baseCurrency,
            targetCurrency=direct_rate.targetCurrency,
            rate=rate.quantize(Decimal('0.01')),
            amount=convert_dto.amount.quantize(Decimal('0.01')),
            convertedAmount=(rate * convert_dto.amount).quantize(Decimal('0.01'))
        )

    def _try_get_inverse_convert(self, convert_dto: ConvertDTO):
        inverse_rate = self._controller.get(f'{convert_dto.base_currency_code}{convert_dto.target_currency_code}')

        rate = (1 / inverse_rate.rate).quantize(Decimal('0.01'))

        return ConvertDetailDTO(
            baseCurrency=inverse_rate.baseCurrency,
            targetCurrency=inverse_rate.targetCurrency,
            rate=rate.quantize(Decimal('0.01')),
            amount=convert_dto.amount.quantize(Decimal('0.01')),
            convertedAmount=(rate * convert_dto.amount).quantize(Decimal('0.01'))
        )

    def _try_get_usd_base_convert(self, convert_dto: ConvertDTO):
        usd_to_base_rate = self._controller.get(f'USD{convert_dto.base_currency_code}')
        usd_to_target_rate = self._controller.get(f'USD{convert_dto.target_currency_code}')

        rate = (usd_to_target_rate.rate / usd_to_base_rate.rate).quantize(Decimal('0.01'))
        return ConvertDetailDTO(
            baseCurrency=usd_to_base_rate.baseCurrency,
            targetCurrency=usd_to_target_rate.targetCurrency,
            rate=rate.quantize(Decimal('0.01')),
            amount=convert_dto.amount.quantize(Decimal('0.01')),
            convertedAmount=(rate * convert_dto.amount).quantize(Decimal('0.01'))
        )


#service = ConvertService(ExchangeRatesController())
#print(service.convert(ConvertDTO('EUR', 'USD', Decimal(1))))
