"""Парсинг цен на сайте Autodoc.ru."""

import requests

from autos.services.price_parsing.domain.parsing_service import TIMEOUT, ParsingService, SpareInfo
from autoworld.env_settings import AUTODOC_LOGIN, AUTODOC_PASSWORD


class AutoDocParsingService(ParsingService):
    """Парсинг данных о запчастях с сайта Autodoc.ru по списку ссылок с помощью функции parse."""

    @classmethod
    def parse(cls, urls: list) -> dict[str, SpareInfo]:
        """Запуск парсинга данных о запчастях согласно списку, возвращает: {ссылка: данные}."""
        try:
            data = {
                "username": AUTODOC_LOGIN,
                "password": AUTODOC_PASSWORD,
                "grant_type": "password"
            }
            response = requests.post(
                "https://auth.autodoc.ru/token",
                data=data,
                timeout=TIMEOUT,
            )
            response_json = response.json()
            headers = {"Authorization": f"Bearer {response_json["access_token"]}"}
            res = {}
            for url in urls:
                spare_credential = url.removeprefix("https://www.autodoc.ru/price/")
                spare_response = requests.get(
                    f"https://webapi.autodoc.ru/api/spareparts/{spare_credential}/3",
                    headers=headers,
                    timeout=TIMEOUT,
                ).json()
                data = SpareInfo(
                    name=spare_response["name"],
                    manufacturer=spare_response["manufacturer"]["name"],
                    price=int(spare_response["inventoryItems"][0]["price"]),
                    partnumber=spare_response["partNumber"],
                    delivery_time=spare_response["inventoryItems"][0]["deliveryDays"],
                )
                res[url] = data
        except Exception as e:  # noqa: BLE001
            print(e)  # noqa: T201
        else:
            return res
