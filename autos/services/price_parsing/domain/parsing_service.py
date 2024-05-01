from abc import ABC, abstractmethod
from typing import NamedTuple

TIMEOUT = 180


class SpareInfo(NamedTuple):
    """Структура данных объектов запчастей."""
    name: str
    manufacturer: str
    partnumber: str
    price: int
    delivery_time: int
    provider: str = None


class ParsingService(ABC):
    """Парсинг данных о запчастях с сайта Autodoc.com по списку ссылок с помощью функции parse."""

    @classmethod
    @abstractmethod
    def parse(cls, urls: list) -> dict[str, SpareInfo]:
        """Запуск парсинга данных о запчастях согласно списку."""
