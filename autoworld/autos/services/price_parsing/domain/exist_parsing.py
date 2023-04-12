import os
import re
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
        sleep(2)
        browser.find_element(by=By.XPATH, value='//*[@id="pnlLogin"]').click()
        sleep(2)
        browser.find_element(by=By.XPATH, value='//*[@id="login"]') \
            .send_keys(os.getenv('EXIST_LOGIN'))  # вставляем логин
        browser.find_element(by=By.XPATH, value='//*[@id="pass"]') \
            .send_keys(os.getenv('EXIST_PASSWORD'))  # вставляем пароль
        sleep(3)
        browser.find_element(by=By.XPATH, value='//*[@id="btnLogin"]').click()

    @staticmethod
    def _detail_parsing(page: str) -> SpareInfo:
        """Парсинг данных конкретной запчасти"""
        soup = BeautifulSoup(page, 'lxml')
        tmp = soup.find('div', string=re.compile('Запрошенный артикул')).find_next('div')
        manufacturer = tmp.find('div', class_='art').text
        name = tmp.find('a', class_='descr').text
        price = int(''.join(tmp.find('span', class_='price').text.split()[:-1]))
        partnumber = tmp.find('div', class_='partno').text.replace(' ', '')

        raw_delivery_time = tmp.find('span', class_='statis').find('a').text.split()[0]
        raw_delivery_time = datetime.strptime(raw_delivery_time, '%d.%m').replace(year=datetime.now().year)
        delivery_time = (raw_delivery_time - datetime.now()).days

        return SpareInfo(name=name,
                         manufacturer=manufacturer,
                         price=price,
                         partnumber=partnumber,
                         delivery_time=delivery_time)

    @classmethod
    def parse(cls, urls: list = None) -> dict[str, SpareInfo]:
        """Запуск парсинга данных о запчастях согласно списку"""
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
                res[url] = cls._detail_parsing(browser.page_source)
                sleep(1)
            return res
        except Exception as err:
            print(f'{type(err)}: {err}')
        finally:
            browser.close()
            browser.quit()
