from django.contrib.auth.models import User

from autos.models import Request, Spare, Auto
from autos.services.price_parsing.domain.autodoc_parsing import AutoDocParsingService
from autos.services.price_parsing.domain.exist_parsing import ExistParsingService
from autos.services.price_parsing.domain.parsing_service import SpareInfo


def add_spare(user_id: str, ad_url: str, ex_url: str, car: int) -> Spare:
    user = User.objects.get(pk=user_id)
    if ad_url and ex_url:
        ad_data = AutoDocParsingService.parse([ad_url])[ad_url]
        ex_data = ExistParsingService.parse([ex_url])[ex_url]
        spare_obj, requests = _make_new_requests_and_spare(user, ad_data, ex_data, car, ad_url, ex_url)
    elif ad_url:
        ad_data = AutoDocParsingService.parse([ad_url])[ad_url]
        spare_obj, requests = _make_new_request_and_spare(user, ad_data, car, ad_url, 'AD')
    else:
        ex_data = ExistParsingService.parse([ex_url])[ex_url]
        spare_obj, requests = _make_new_request_and_spare(user, ex_data, car, ex_url, 'EX')
    Request.objects.bulk_create(requests)
    return spare_obj


def _make_new_request_and_spare(user: User, parsing_data: SpareInfo, car: int,
                                url: str, site: str) -> tuple[Spare, list[Request]]:
    """Создание объекта новой запчасти и запроса на одном из сайтов"""
    parameters = {'autodoc_URL': url} if site == 'AD' else {'exist_URL': url}
    spare_obj = Spare.objects.create(name=parsing_data.name,
                                     car=Auto.objects.get(pk=car),
                                     manufacturer=parsing_data.manufacturer,
                                     partnumber=parsing_data.partnumber,
                                     **parameters)
    req_obj = Request(spare=spare_obj,
                      site=site,
                      author=user,
                      price=parsing_data.price,
                      delivery_time=parsing_data.delivery_time)
    return spare_obj, [req_obj]


def _make_new_requests_and_spare(user: User, ad_data: SpareInfo, ex_data: SpareInfo, car: int,
                                 ad_url: str, ex_url: str) -> tuple[Spare, list[Request]]:
    """Создание объекта новой запчасти и запросов на обоих сайтах"""
    spare_obj = Spare.objects.create(name=ad_data.name,
                                     car=Auto.objects.get(pk=car),
                                     manufacturer=ad_data.manufacturer,
                                     partnumber=ad_data.partnumber,
                                     autodoc_URL=ad_url,
                                     exist_URL=ex_url)
    new_request_objects = [
        Request(spare=spare_obj,
                site='AD',
                author=user,
                price=ad_data.price,
                delivery_time=ad_data.delivery_time),
        Request(spare=spare_obj,
                site='EX',
                author=user,
                price=ex_data.price,
                delivery_time=ex_data.delivery_time),
    ]
    return spare_obj, new_request_objects
