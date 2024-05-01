from datetime import datetime

import bs4.element
import requests
from bs4 import BeautifulSoup

from autos.services.price_parsing.domain.autodoc_parsing import SpareInfo
from autos.services.price_parsing.domain.parsing_service import TIMEOUT, ParsingService

COOKIE = {"_go": "957"}


class ExistParsingService(ParsingService):
    """Парсинг данных о запчастях с сайта Exist.ru по списку ссылок с помощью функции parse."""

    @classmethod
    def _detail_parsing(cls, page: str) -> SpareInfo | None:
        """Парсинг данных конкретной запчасти."""
        soup = BeautifulSoup(page, "lxml")
        try:
            tmp = soup.find("div", class_="page-blocks page-blocks--padding page-content-wrapper")
            manufacturer = tmp.find("div", itemprop="brand").text
            partnumber = tmp.find("h1", itemprop="name").text.replace(manufacturer, "").strip().replace(" ", "")
            name = tmp.find("div", class_="subtitle").text
            price_block = tmp.find("div", id="prices")
            price, delivery_time = cls._get_min_price(price_block)
        except (IndexError, AttributeError):
            return None
        return SpareInfo(
            name=name,
            manufacturer=manufacturer,
            price=price,
            partnumber=partnumber,
            delivery_time=delivery_time
        )

    @staticmethod
    def _get_min_price(soup: bs4.element.Tag) -> tuple[int, int]:
        """Поиск минимальной цены на товар и вычисление количество дней доставки, возвращает: (цена, доставка)."""
        all_price_blocks = soup.find_all("div", class_="pricerow")
        all_prices = {
            int(price_block.find("meta", itemprop="price").get("content")): price_block
            for price_block in all_price_blocks
        }
        min_price = min(all_prices)
        raw_delivery_time = all_prices[min_price].find("span", class_="statis").text.split()[0]
        raw_delivery_time = datetime.strptime(raw_delivery_time, "%d.%m.%Y")  # noqa: DTZ007
        delivery_time = (raw_delivery_time - datetime.now()).days  # noqa: DTZ005
        return min_price, delivery_time

    @classmethod
    def parse(cls, urls: list | None = None) -> dict[str, SpareInfo]:
        """Запуск парсинга данных о запчастях согласно списку, возвращает: {ссылка: данные}."""
        res = {}
        try:
            for url in urls:
                response = requests.get(url, cookies=COOKIE, timeout=TIMEOUT)
                res[url] = cls._detail_parsing(response.text)
        except Exception as e:  # noqa: BLE001
            print(e)  # noqa: T201
        else:
            return res
