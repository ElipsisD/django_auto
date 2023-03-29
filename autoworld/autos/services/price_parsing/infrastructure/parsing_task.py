from django.contrib.auth.models import User

from autos.models import Spare, Request
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


def single_request(user_id: str, url: str) -> None:
    user = User.objects.get(pk=user_id)
    new_requests_data = AutoDocParsingService.parse(list(url))
    new_requests_data = new_requests_data[url]
    Request.objects.create(spare=question,
                           author=user,
                           price=new_requests_data.price,
                           delivery_time=new_requests_data.delivery_time)
