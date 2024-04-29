from abc import ABC, abstractmethod
from typing import NamedTuple

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


class SpareInfo(NamedTuple):
    """Структура данных объектов запчастей"""
    name: str
    manufacturer: str
    partnumber: str
    price: int
    delivery_time: int
    provider: str = None


class ParsingService(ABC):
    """Парсинг данных о запчастях с сайта Autodoc.com по списку ссылок с помощью функции parse"""

    @staticmethod
    def _make_service() -> webdriver:
        """Создание и настройка webdriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features-AutomationControlled')  # отключение режима WebDriver
        return webdriver.Remote(
            "http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME,
            options=options
        )

    @staticmethod
    @abstractmethod
    def _auth(browser: webdriver) -> None:
        """Авторизация на сайте"""
        pass

    @staticmethod
    @abstractmethod
    def _detail_parsing(page: str) -> SpareInfo:
        """Парсинг данных конкретной запчасти"""
        pass

    @classmethod
    @abstractmethod
    def parse(cls, urls: list) -> dict[str, SpareInfo]:
        """Запуск парсинга данных о запчастях согласно списку"""
        pass
