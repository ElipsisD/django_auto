"""Парсинг цен на сайте Autodoc.ru"""
import os
import re
from time import sleep
from typing import NamedTuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class SpareInfo(NamedTuple):
    """Структура данных объектов запчастей"""
    name: str
    manufacturer: str
    partnumber: str
    # autodoc_URL: str
    price: int
    delivery_time: int
    provider: str


class AutoDocParsingService:
    """Парсинг данных о запчастях с сайта Autodoc.com по списку ссылок с помощью функции parse"""

    @staticmethod
    def _make_service() -> webdriver:
        """Создание и настройка webdriver"""
        browser = webdriver.Remote('http://selenium:4444', desired_capabilities=DesiredCapabilities.CHROME)
        return browser

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
    def _detail_parsing(page: str) -> SpareInfo:
        """Парсинг данных конкретной запчасти"""
        soup = BeautifulSoup(page, 'lxml')
        tmp = soup.find('h3', string=re.compile('Все предложения запрошенного номера')) \
            .find_parent('app-price-table')
        manufacturer = tmp.find('a', class_='company_info_link').text
        name = tmp.find('div', class_='title-name').text
        price = int(tmp.find('td', class_='price').find('span').text.split('.')[0].replace(' ', ''))
        partnumber = tmp.find('div', class_='title-part').text.replace(manufacturer, '').replace(' ', '')
        delivery_time = int(tmp.find('td', class_='delivery').find('span').text)
        provider = tmp.find('span', class_='direction-mob direction').text
        return SpareInfo(name=name,
                         manufacturer=manufacturer,
                         price=price,
                         partnumber=partnumber,
                         delivery_time=delivery_time,
                         provider=provider)

    @classmethod
    def parse(cls, urls: list) -> dict[str, SpareInfo]:
        """Запуск парсинга данных о запчастях согласно списку"""
        browser = cls._make_service()
        try:
            cls._auth(browser)
            sleep(2)
            res = {}
            for url in urls:
                browser.get(url)
                WebDriverWait(browser, timeout=20).until(
                    lambda x: x.find_element(by=By.TAG_NAME, value='tbody'))
                res[url] = cls._detail_parsing(browser.page_source)
                sleep(1)
            return res
        except Exception as err:
            print(err)
        finally:
            browser.close()
            browser.quit()


# print(*AutoDocParsingService.parse(
#     ['https://www.autodoc.ru/price/4/W7008', 'https://www.autodoc.ru/price/647/866141Y000']).values(), sep='\n')
# print(autodoc_parse('W7008'))
# print(autodoc_parse('2074151'))



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
