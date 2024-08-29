from urllib.parse import urlparse

from controller.currencies_controller import CurrenciesController
from controller.exchange_rates_controller import ExchangeRatesController
from exceptions import BadURLError, MissingCurrencyCodeError


class Router:
    def __init__(self):
        self._currencies_controller = CurrenciesController()
        self._exchange_rates_controller = ExchangeRatesController()

        self._router = {
            'GETcurrencies': {
                'controller': self._currencies_controller.get,
                'with_id': False
            },
            'GETcurrency': {
                'controller': lambda data: self._currencies_controller.get(data),
                'with_id': True
            },
            'POSTcurrencies': {
                'controller': lambda data: self._currencies_controller.insert(data),
                'with_id': False
            },
            'GETexchangeRates': {
                'controller': self._exchange_rates_controller.get,
                'with_id': False
            },
            'GETexchangeRate': {
                'controller': lambda data: self._exchange_rates_controller.get(data),
                'with_id': True
            },
            'POSTexchangeRates': {
                'controller': lambda data: self._exchange_rates_controller.insert(data),
                'with_id': False
            },
            'PATCHexchangeRate': {
                'controller': lambda codes: lambda data: self._exchange_rates_controller.update(codes, data),
                'with_id': True
            },
            'GETexchange': {
                'controller': lambda data: self._exchange_rates_controller.convert(data),
                'with_id': False
            }
        }

    def get(self, command: str, path: str):
        try:
            segments, query_params = self.parse_url(path)
            route = self._try_get_route(f'{command}{segments[0]}')
        except IndexError:
            raise BadURLError(url=path)

        controller = route['controller']
        with_id = route['with_id']

        if command == 'GET':
            if with_id and len(segments) == 2:
                return controller(segments[1])
            elif with_id:
                raise MissingCurrencyCodeError
            elif query_params:
                return controller(query_params)

            return controller()
        elif command == 'POST':
            return controller
        elif command == 'PATCH':
            if with_id and len(segments) == 2:
                return controller(segments[1])
            elif with_id:
                raise MissingCurrencyCodeError

    def _try_get_route(self, path: str):
        route = self._router.get(path)
        if not route:
            raise BadURLError(path)
        return route

    @staticmethod
    def parse_url(url):
        parsed_url = urlparse(url)

        path_segments = parsed_url.path.split('/')
        query_params = parsed_url.query

        return [s for s in path_segments if s], query_params


