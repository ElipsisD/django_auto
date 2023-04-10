import os

from django.conf import settings
from django.core.files import File

from autos.models import Request, Spare
from autos.services.plotting.domain.making_graphs import make_spare_fig, SpareRequestsData


def make_graphs_for_all_spares():
    """Создание графиков для всех запчастей"""
    spares = Spare.objects.all()
    for spare in spares:
        _make_graph(spare)


def make_graph_for_spare(spare_id: int):
    """Создание графика для конкретной запчасти"""
    spare = Spare.objects.get(id=spare_id)
    _make_graph(spare)


def _make_graph(spare: Spare):
    """Получение данных о запчасти и создание файла графика"""
    data = _get_data_for_graph(spare)
    graph_path = make_spare_fig(spare.partnumber, data)
    with open(graph_path, 'rb') as f:
        graph_name = graph_path.split('/')[-1]
        all_graphs_path = os.path.join(settings.MEDIA_ROOT, 'graphs')
        if os.path.exists(os.path.join(all_graphs_path, graph_name)):
            os.remove(os.path.join(all_graphs_path, graph_name))
        spare.price_graph = File(f, name=graph_name)
        spare.save(update_fields=['price_graph'])
        os.remove(graph_path)


def _get_data_for_graph(spare: Spare) -> SpareRequestsData:
    """Компоновка данных о ценах и датах запросов для запчасти"""
    requests = Request.objects.filter(spare=spare).only('price', 'time_create')
    prices, dates = [], []
    for request in requests:
        prices.append(request.price)
        dates.append(request.time_create)
    return SpareRequestsData(prices, dates)
