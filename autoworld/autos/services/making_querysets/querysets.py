from django.db.models import Max, QuerySet

from autos.models import Request


def last_request_objects() -> QuerySet:
    """Возвращает данные о последних запросах всех запчастей"""
    actual_dates = Request.objects.values('spare_id').annotate(date=Max('time_create'))
    actual_dates = [el['date'] for el in actual_dates]
    return Request.objects.filter(time_create__in=actual_dates)