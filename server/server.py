from http.server import HTTPServer, BaseHTTPRequestHandler

from router.router import Router
from view.view_to_json import ViewToJson
from exceptions import (DatabaseAccessError, RecordNotFoundError, MissingCurrencyCodeError, BadURLError,
                        ImpossibleConvertError, InsertAlreadyExistsRecordError, CurrenciesNotExistsError)


class Handler(BaseHTTPRequestHandler):
    _ROUTER = Router()
    _view = ViewToJson()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            response = self._ROUTER.get(command=self.command, path=self.path)
            self._send_response(self._view.dto_to_json(response), status_code=200)
        except DatabaseAccessError as e:
            self._send_response(self._view.error_to_json(e), status_code=500)
        except RecordNotFoundError as e:
            self._send_response(self._view.error_to_json(e), status_code=404)
        except BadURLError as e:
            self._send_response(self._view.error_to_json(e), status_code=404)
        except ImpossibleConvertError as e:
            self._send_response(self._view.error_to_json(e), status_code=400)
        except MissingCurrencyCodeError as e:
            self._send_response(self._view.error_to_json(e), status_code=400)

    def do_POST(self):
        try:
            data = self._get_data()
            response = self._ROUTER.get(command=self.command, path=self.path)(data)
            self._send_response(self._view.dto_to_json(response), status_code=201)
        except DatabaseAccessError as e:
            self._send_response(self._view.error_to_json(e), status_code=500)
        except InsertAlreadyExistsRecordError as e:
            self._send_response(self._view.error_to_json(e), status_code=409)
        except RecordNotFoundError as e:
            self._send_response(self._view.error_to_json(e), status_code=404)
        except CurrenciesNotExistsError as e:
            self._send_response(self._view.error_to_json(e), status_code=404)
        except BadURLError as e:
            self._send_response(self._view.error_to_json(e), status_code=404)
        except MissingCurrencyCodeError as e:
            self._send_response(self._view.error_to_json(e), status_code=400)

    def do_PATCH(self):
        try:
            data = self._get_data()
            response = self._ROUTER.get(command=self.command, path=self.path)(data)
            self._send_response(self._view.dto_to_json(response), status_code=200)
        except DatabaseAccessError as e:
            self._send_response(self._view.error_to_json(e), status_code=500)
        except RecordNotFoundError as e:
            self._send_response(self._view.error_to_json(e), status_code=404)
        except MissingCurrencyCodeError as e:
            self._send_response(self._view.error_to_json(e), status_code=400)

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_headers()
        self.end_headers()

    def _send_response(self, json_data: str, status_code: int, content_type: str = None):
        self.send_response(status_code)

        self._send_headers()
        if content_type:
            self.send_header('Content-Type', content_type)
        self.end_headers()

        self.wfile.write(bytes(json_data, 'utf-8'))

    def _send_headers(self):
        self.send_header(
            keyword='Access-Control-Allow-Credentials',
            value='true'
        )
        self.send_header(
            keyword="Access-Control-Allow-Origin",
            value='*'
        )
        self.send_header(
            keyword="Access-Control-Allow-Methods",
            value='GET, POST, OPTIONS, PATCH'
        )
        self.send_header(
            keyword='Access-Control-Allow-Headers',
            value='Content-Type'
        )

    def _get_data(self):
        return self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8")


def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Handler)
    print('Server running at http://localhost:8000')
    httpd.serve_forever()


run()
