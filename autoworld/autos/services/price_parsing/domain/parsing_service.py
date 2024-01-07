import os
from abc import ABC, abstractmethod
from typing import NamedTuple

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from autoworld.settings import COMMAND_EXECUTOR, BASE_DIR


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
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')  # работа браузера в тихом режиме
        options.add_experimental_option("detach", True)  # оставить браузер включенным
        options.add_argument('--disable-blink-features-AutomationControlled')  # отключение режима WebDriver
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # browser = webdriver.Remote(COMMAND_EXECUTOR, desired_capabilities=DesiredCapabilities.CHROME)
        return browser

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


# options = webdriver.ChromeOptions()
# options = Options()
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless')  # работа браузера в тихом режиме
# options.headless = True  # работа браузера в тихом режиме
# options.add_experimental_option("detach", True)  # оставить браузер включенным
# options.add_argument('--disable-blink-features-AutomationControlled')  # отключение режима WebDriver
# options.add_argument('user-agent=Mozilla/5.0 (Windows NT 5.1) '
#                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36')
# driver = Service(os.path.join(BASE_DIR, 'chromedriver.exe'))
# browser = webdriver.Chrome(service=driver, options=options)
# browser = WebDriver(options=options)
