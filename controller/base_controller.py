from abc import ABC, abstractmethod
from urllib.parse import parse_qs

from exceptions import MissingFieldError


class Controller(ABC):
    @abstractmethod
    def _DAO(self):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def insert(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

    @staticmethod
    def _parse_data(data, necessary_fields: tuple['str', ...]):
        form_fields = parse_qs(data)

        if any(necessary_field not in form_fields for necessary_field in necessary_fields):
            raise MissingFieldError(fields=necessary_fields)

        return {key: value[0] for key, value in form_fields.items()}






