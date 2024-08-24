import json
from decimal import Decimal

from DTO import CurrencyIDDTO, ExchangeRateDetailDTO, ConvertDetailDTO


class ViewToJson:

    def dto_to_json(
            self, dto: CurrencyIDDTO | ExchangeRateDetailDTO | ConvertDetailDTO |
            list[CurrencyIDDTO] | list[ExchangeRateDetailDTO]
    ):
        #if isinstance(dto, (CurrencyIDDTO, ExchangeRateDetailDTO, ConvertDetailDTO)):
        #    return json.dumps(dto.__dict__, ensure_ascii=False, indent=4)
        #elif all(isinstance(d, (CurrencyIDDTO, ExchangeRateDetailDTO)) for d in dto):
        #    return json.dumps([d.__dict__ for d in dto], ensure_ascii=False, indent=4)
        #else:
        #    raise TypeError("Дописать!")
        if isinstance(dto, (CurrencyIDDTO, ExchangeRateDetailDTO, ConvertDetailDTO)):
            return json.dumps(self._dto_to_dict(dto), ensure_ascii=False, indent=4)
        elif all(isinstance(d, (CurrencyIDDTO, ExchangeRateDetailDTO)) for d in dto):
            return json.dumps([self._dto_to_dict(d) for d in dto], ensure_ascii=False, indent=4)
        else:
            raise TypeError("")

    @staticmethod
    def error_to_json(error):
        return json.dumps(
            {'message': str(error)}, ensure_ascii=False, indent=4
        )

    @staticmethod
    def _dto_to_dict(dto_obj):
        res = {}
        for k, v in dto_obj.__dict__.items():
            if isinstance(v, Decimal):
                res[k] = str(v)
            else:
                res[k] = v
        return res
