from django.contrib.auth.models import User

from autos.models import Spare, Request, Auto
from autos.services.making_querysets.querysets import last_request_objects
from autos.services.price_parsing.domain.autodoc_parsing import AutoDocParsingService


def make_request(user_id: int) -> None:
    user = User.objects.get(pk=user_id)
    spares = Spare.objects.all().filter(autodoc_URL__isnull=False)
    spares_objects = {el.autodoc_URL: el for el in spares}
    new_requests_data = AutoDocParsingService.parse(list(spares_objects.keys()))
    previous_data = last_request_objects().values('spare', 'price')
    previous_data = {el['spare']: el['price'] for el in previous_data}
    objects_to_create = []
    for url, spare_info_obj in new_requests_data.items():
        objects_to_create.append(Request(spare=spares_objects[url],
                                         author=user,
                                         price=spare_info_obj.price,
                                         delivery_time=spare_info_obj.delivery_time,
                                         difference=previous_data[spares_objects[url].pk] - spare_info_obj.price))
    Request.objects.bulk_create(objects_to_create)


def add_spare(user_id: int, url: str, car: int) -> Spare:
    user = User.objects.get(pk=user_id)
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
