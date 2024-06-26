import os

from django.conf import settings
from django.core.files import File

from autos.models import Request, Spare
from autos.services.plotting.domain.making_graphs import SpareRequestsData, make_spare_fig


def make_graphs_for_all_spares() -> None:
    """Создание графиков для всех запчастей."""
    spares = Spare.objects.all()
    for spare in spares:
        _make_graph(spare)


def make_graph_for_spare(spare_id: int) -> None:
    """Создание графика для конкретной запчасти."""
    spare = Spare.objects.get(id=spare_id)
    _make_graph(spare)


def _make_graph(spare: Spare) -> None:
    """Получение данных о запчасти и создание файла графика."""
    data = _get_data_for_graph(spare)
    graph_path = make_spare_fig(spare.partnumber, data)
    with open(graph_path, "rb") as f:
        graph_name = graph_path.split("/")[-1]
        all_graphs_path = os.path.join(settings.MEDIA_ROOT, "graphs")
        if os.path.exists(os.path.join(all_graphs_path, graph_name)):
            os.remove(os.path.join(all_graphs_path, graph_name))
        spare.price_graph = File(f, name=graph_name)
        spare.save(update_fields=["price_graph"])
        os.remove(graph_path)


def _get_data_for_graph(spare: Spare) -> SpareRequestsData:
    """Компоновка данных о ценах и датах запросов для запчасти."""
    requests = Request.objects.filter(spare=spare).only("site", "price", "time_create")
    AD_prices, EX_prices, AD_dates, EX_dates = [], [], [], []
    for request in requests:
        if request.site == "AD":
            AD_prices.append(request.price)
            AD_dates.append(request.time_create)
        if request.site == "EX":
            EX_prices.append(request.price)
            EX_dates.append(request.time_create)
    return SpareRequestsData(AD_prices, EX_prices, AD_dates, EX_dates)
