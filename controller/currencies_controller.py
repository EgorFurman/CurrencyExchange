from controller.base_controller import Controller
from DAO.currincies_DAO import CurrenciesDAO
from DTO.currency_DTO import CurrencyDTO, CurrencyIDDTO


class CurrenciesController(Controller):
    _DAO = CurrenciesDAO()
    _NECESSARY_POST_FIELDS = ('code', 'name', 'sign')

    def get(self, code: str = None) -> CurrencyIDDTO | list[CurrencyIDDTO]:
        if code:
            return self._to_DTO(self._DAO.get_by_code(code))
        return [self._to_DTO(r) for r in self._DAO.get_all()]

    def insert(self, data: str) -> CurrencyIDDTO:
        parsed_data = self._parse_data(data=data, necessary_fields=self._NECESSARY_POST_FIELDS)
        response = self._DAO.insert(
            CurrencyDTO(code=parsed_data['code'], name=parsed_data['name'], sign=parsed_data['sign'])
        )

        return self._to_DTO(response)

    def update(self, *args, **kwargs):
        ...

    def delete(self,  *args, **kwargs):
        ...

    @staticmethod
    def _to_DTO(response: tuple[int, str, str, str]):
        return CurrencyIDDTO(*response)

    #def _parse_data(self, data, fields):
    #    form_fields = parse_qs(data)
#
    #    if any(necessary_field not in form_fields for necessary_field in self._NECESSARY_FIELDS):
    #        raise MissingFieldError(fields=self._NECESSARY_FIELDS)
#
    #    return {key: value[0] for key, value in form_fields.items()}


