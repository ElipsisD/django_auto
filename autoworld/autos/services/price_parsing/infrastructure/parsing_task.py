from django.contrib.auth.models import User

from autos.models import Spare, Request, Auto
from autos.services.making_querysets.querysets import last_request_objects
from autos.services.price_parsing.domain.autodoc_parsing import AutoDocParsingService
from autos.services.price_parsing.domain.exist_parsing import ExistParsingService


def make_request(user: User) -> None:
    autodoc_new_objects = make_autodoc_request(user)
    exist_new_objects = make_exist_request(user)
    new_request_objects = autodoc_new_objects + exist_new_objects
    Request.objects.bulk_create(new_request_objects)


def add_spare(user: User, url: str, car: int) -> Spare:
    new_request_data = AutoDocParsingService.parse([url])
    new_request_data = new_request_data[url]
    spare_obj = Spare.objects.create(name=new_request_data.name,
                                     car=Auto.objects.get(pk=car),
                                     manufacturer=new_request_data.manufacturer,
                                     partnumber=new_request_data.partnumber,
                                     autodoc_URL=url)
    Request.objects.create(spare=spare_obj,
                           author=user,
                           price=new_request_data.price,
                           delivery_time=new_request_data.delivery_time)
    return spare_obj


def make_autodoc_request(user: User) -> list[Request]:
    spares = Spare.objects.all().filter(autodoc_URL__isnull=False)
    spares_objects = {el.autodoc_URL: el for el in spares}
    new_requests_data = AutoDocParsingService.parse(list(spares_objects.keys()))
    previous_data = last_request_objects().filter(site='AD').values('spare', 'price')
    previous_data = {el['spare']: el['price'] for el in previous_data}
    objects_to_create = []
    for url, spare_info_obj in new_requests_data.items():
        objects_to_create.append(Request(spare=spares_objects[url],
                                         site='AD',
                                         author=user,
                                         price=spare_info_obj.price,
                                         delivery_time=spare_info_obj.delivery_time,
                                         difference=spare_info_obj.price -
                                                    previous_data.get(spares_objects[url].pk, 0)))
    return objects_to_create


def make_exist_request(user: User) -> list[Request]:
    print(ExistParsingService.parse(['https://www.exist.ru/Price/?pid=7920D19A']))
    # spares = Spare.objects.all().filter(exist_URL__isnull=False)
    # spares_objects = {el.exist_URL: el for el in spares}
    # new_requests_data = ExistParsingService.parse(list(spares_objects.keys()))
    # previous_data = last_request_objects().filter(site='EX').values('spare', 'price')
    # previous_data = {el['spare']: el['price'] for el in previous_data}
    # objects_to_create = []
    # for url, spare_info_obj in new_requests_data.items():
    #     objects_to_create.append(Request(spare=spares_objects[url],
    #                                      site='EX',
    #                                      author=user,
    #                                      price=spare_info_obj.price,
    #                                      delivery_time=spare_info_obj.delivery_time,
    #                                      difference=spare_info_obj.price -
    #                                                 previous_data.get(spares_objects[url].pk, 0)))
    # return objects_to_create
