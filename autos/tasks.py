from autos.services.plotting.infrastructure.making_graphs_task import make_graph_for_spare, make_graphs_for_all_spares
from autos.services.price_parsing.infrastructure.add_spare_task import add_spare
from autos.services.price_parsing.infrastructure.parsing_task import make_request
from celery_app import app


@app.task(bind=True, max_retries=3)
def do_make_request(self, user: str) -> None:
    """Выполнения новых запросов для всех запчастей."""
    try:
        make_request(user)
    except Exception as err:
        self.retry(exc=err, countdown=10)
    make_graphs_for_all_spares()


@app.task
def do_add_spare(user: str, ad_url: str, ex_url: str, car: int) -> None:
    """Выполнение запроса для одной запчасти."""
    spare = add_spare(user, ad_url, ex_url, car)
    make_graph_for_spare(spare.pk)

# docker-compose run --rm web-app sh -c "python3 manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json"
