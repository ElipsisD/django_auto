from django.contrib.auth.models import User

from autos.models import Spare, Request, Auto
from autos.services.price_parsing.domain.autodoc_parsing import AutoDocParsingService


def make_request(user_id: str) -> None:
    user = User.objects.get(pk=user_id)
    spares = Spare.objects.all().filter(autodoc_URL__isnull=False)
    print(spares)
    spares_objects = {el.autodoc_URL: el for el in spares}
    new_requests_data = AutoDocParsingService.parse(list(spares_objects.keys()))
    objects_to_create = []
    for url, spare_info_obj in new_requests_data.items():
        objects_to_create.append(Request(spare=spares_objects[url],
                                         author=user,
                                         price=spare_info_obj.price,
                                         delivery_time=spare_info_obj.delivery_time))
    print(objects_to_create)
    Request.objects.bulk_create(objects_to_create)


def add_spare(user_id: str, url: str, car: str) -> None:
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
