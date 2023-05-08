import os
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from autos.services.price_parsing.domain.autodoc_parsing import SpareInfo
from autos.services.price_parsing.domain.parsing_service import ParsingService


class ExistParsingService(ParsingService):
    """Парсинг данных о запчастях с сайта Exist.ru по списку ссылок с помощью функции parse"""

    @staticmethod
    def _auth(browser: webdriver) -> None:
        """Авторизация на сайте"""
        browser.get('https://www.exist.ru/')
        WebDriverWait(browser, timeout=10).until(
            lambda x: x.find_element(by=By.TAG_NAME, value='div'))
        browser.find_element(by=By.XPATH, value='//*[@id="pnlLogin"]').click()
        sleep(1)
        browser.find_element(by=By.XPATH, value='//*[@id="login"]') \
            .send_keys(os.getenv('EXIST_LOGIN'))  # вставляем логин
        browser.find_element(by=By.XPATH, value='//*[@id="pass"]') \
            .send_keys(os.getenv('EXIST_PASSWORD'))  # вставляем пароль
        sleep(1)
        browser.find_element(by=By.XPATH, value='//*[@id="btnLogin"]').click()

    @classmethod
    def _detail_parsing(clc, page: str) -> SpareInfo | None:
        """Парсинг данных конкретной запчасти"""
        soup = BeautifulSoup(page, 'lxml')
        try:
            tmp = soup.find('h1', class_='fn identifier').text.split()
            manufacturer = tmp[0]
            partnumber = ''.join(tmp[1:])
            name = soup.find('div', class_='subtitle').text
            price, delivery_time = clc._get_min_price(soup)
        except (IndexError, AttributeError):
            return None
        return SpareInfo(name=name,
                         manufacturer=manufacturer,
                         price=price,
                         partnumber=partnumber,
                         delivery_time=delivery_time)

    @staticmethod
    def _get_min_price(soup: BeautifulSoup) -> tuple[int, int]:
        """Поиск минимальной цены на товар и вычисление количество дней доставки, возвращает: (цена, доставка)"""
        all_price_block = soup.find_all('div', class_='pricerow')
        min_price_block = 0
        min_price = 1_000_000
        for i, div in enumerate(all_price_block):
            price = int(''.join(div.find('span', class_='price ucatprc').text.split()[:-1]))
            if price < min_price:
                min_price = price
                min_price_block = i
        raw_delivery_time = all_price_block[min_price_block].find('span', class_='statis').text.split()[0]
        try:
            raw_delivery_time = datetime.strptime(raw_delivery_time, '%d.%m').replace(year=datetime.now().year)
            delivery_time = (raw_delivery_time - datetime.now()).days
        except Exception as err:
            print(err)
            weekday = {'пн': 1, 'вт': 2, 'ср': 3, 'чт': 4, 'пт': 5, 'сб': 6, 'вс': 7}[raw_delivery_time.lower()]
            delivery_time = weekday - datetime.now().isoweekday() \
                if weekday - datetime.now().isoweekday() > 0 \
                else weekday - datetime.now().isoweekday() + 7
        return min_price, delivery_time

    @classmethod
    def parse(cls, urls: list = None) -> dict[str, SpareInfo]:
        """Запуск парсинга данных о запчастях согласно списку, возвращает: {ссылка: данные}"""
        browser = cls._make_service()
        try:
            cls._auth(browser)
            sleep(2)
            res = {}
            for url in urls:
                browser.get(url)
                for _ in range(3):
                    try:
                        WebDriverWait(browser, timeout=10).until(
                            lambda x: x.find_element(by=By.TAG_NAME, value='div'))
                        break
                    except TimeoutException:
                        browser.refresh()
                if data := cls._detail_parsing(browser.page_source):
                    res[url] = data
                sleep(1)
            return res
        except Exception as err:
            print(f'{type(err)}: {err}')
        finally:
            browser.close()
            browser.quit()
