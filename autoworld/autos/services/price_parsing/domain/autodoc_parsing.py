"""Парсинг цен на сайте Autodoc.ru"""
import os
import re
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from autos.services.price_parsing.domain.parsing_service import ParsingService, SpareInfo


class AutoDocParsingService(ParsingService):
    """Парсинг данных о запчастях с сайта Autodoc.ru по списку ссылок с помощью функции parse"""

    @staticmethod
    def _auth(browser: webdriver) -> None:
        """Авторизация на сайте"""
        browser.get('https://www.autodoc.ru/')
        sleep(2)
        browser.find_element(by=By.XPATH, value='//*[@id="loginInfo"]/div/a').click()
        sleep(2)
        browser.find_element(by=By.XPATH, value='//*[@id="Login"]') \
            .send_keys(os.getenv('AUTODOC_LOGIN'))  # вставляем логин
        browser.find_element(by=By.XPATH, value='//*[@id="Password"]') \
            .send_keys(os.getenv('AUTODOC_PASSWORD'))  # вставляем пароль
        sleep(3)
        browser.find_element(by=By.XPATH, value='//*[@id="submit_logon_page"]').click()

    @staticmethod
    def _detail_parsing(page: str) -> SpareInfo | None:
        """Парсинг данных конкретной запчасти"""
        soup = BeautifulSoup(page, 'lxml')
        try:
            tmp = soup.find('h3', string=re.compile('Все предложения запрошенного номера')) \
                .find_parent('app-price-table')
            manufacturer = tmp.find('a', class_='company_info_link').text
            name = tmp.find('div', class_='title-name').text
            price = int(tmp.find('td', class_='price').find('span').text.split('.')[0].replace(' ', ''))
            partnumber = tmp.find('div', class_='title-part').text.replace(manufacturer, '').replace(' ', '')
            delivery_time = int(tmp.find('td', class_='delivery').find('span').text)
            provider = tmp.find('span', class_='direction-mob direction').text
        except AttributeError:
            return None
        return SpareInfo(name=name,
                         manufacturer=manufacturer,
                         price=price,
                         partnumber=partnumber,
                         delivery_time=delivery_time,
                         provider=provider)

    @classmethod
    def parse(cls, urls: list) -> dict[str, SpareInfo]:
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
                        WebDriverWait(browser, timeout=15).until(
                            lambda x: x.find_element(by=By.TAG_NAME, value='tbody'))
                        break
                    except TimeoutException:
                        browser.get(url)
                if data := cls._detail_parsing(browser.page_source):
                    res[url] = data
                sleep(1)
            return res
        except Exception as err:
            print(f'{type(err)}: {err}')
        finally:
            browser.close()
            browser.quit()
