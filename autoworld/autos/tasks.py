from celery import shared_task
from celery_singleton import Singleton

from autos.models import Auto
from autos.services.price_parsing.infrastructure.parsing_task import make_request, add_spare
from celery_app import app


# @shared_task(base=Singleton)
@app.task
def do_make_request(user_id: int):
    """Выполнения новых запросов для всех запчастей"""
    make_request(user_id)


@app.task
def do_add_spare(user_id: int, url: str, car: int):
    """Выполнение запроса для одной запчасти"""
    add_spare(user_id, url, car)

# docker-compose run --rm web-app sh -c "python manage.py dumpdata auth.user --indent 2 > db.json"
