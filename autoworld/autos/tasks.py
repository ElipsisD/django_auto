from celery import shared_task
from celery_singleton import Singleton

from autos.services.price_parsing.infrastructure.parsing_task import make_request, single_request
from celery_app import app


# @shared_task(base=Singleton)
@app.task
def do_make_request(user_id):
    make_request(user_id)


@app.task
def do_single_request(user_id, url):
    single_request(user_id, url)

# docker-compose run --rm web-app sh -c "manage.py dumpdata auth.user --indent 2 > db.json"
