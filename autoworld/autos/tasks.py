from celery import shared_task
from celery_singleton import Singleton
from django.contrib.auth.models import User

from autos.models import Auto
from autos.services.plotting.infrastructure.making_graphs_task import make_graphs_for_all_spares, make_graph_for_spare
from autos.services.price_parsing.domain.exist_parsing import ExistParsingService
from autos.services.price_parsing.infrastructure.parsing_task import make_request, add_spare
from celery_app import app


# @shared_task(base=Singleton)
@app.task
def do_make_request(user: User):
    """Выполнения новых запросов для всех запчастей"""
    make_request(user)
    make_graphs_for_all_spares()

@app.task
def test_example():
    ExistParsingService.parse()


@app.task
def do_add_spare(user: User, url: str, car: int):
    """Выполнение запроса для одной запчасти"""
    spare = add_spare(user, url, car)
    make_graph_for_spare(spare.pk)

# docker-compose run --rm web-app sh -c "python manage.py dumpdata auth.user --indent 2 > db.json"
