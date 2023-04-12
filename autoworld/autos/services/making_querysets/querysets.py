from django.db.models import Max, QuerySet

from autos.models import Request, Spare


def last_request_objects() -> QuerySet:
    """Возвращает данные о последних запросах всех запчастей"""
    actual_dates = Request.objects.values('spare_id', 'site').annotate(date=Max('time_create'))
    actual_dates = [el['date'] for el in actual_dates]
    return Request.objects.filter(time_create__in=actual_dates)


def get_actual_prices() -> list[list[Request | None, Request | None]]:
    """Возвращает список списков из последних актуальных запросов
    на каждом сайте (если такие запросы существуют) в формате ['AD', 'EX']"""
    queryset = last_request_objects().select_related('spare__car')
    requests = []
    EX_objects = {el.spare.pk: el for el in queryset.filter(site='EX')}
    AD_objects = {el.spare.pk: el for el in queryset.filter(site='AD')}
    for spare in Spare.objects.all().order_by('name'):
        tmp = [None, None]
        if spare.pk in AD_objects:
            tmp[0] = AD_objects[spare.pk]
        if spare.pk in EX_objects:
            tmp[1] = EX_objects[spare.pk]
        requests.append(tmp)
    return requests
