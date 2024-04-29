import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoworld.settings')

app = Celery('autoworld')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    '3-time-a-day': {
        'task': 'autos.tasks.do_make_request',
        'schedule': crontab(minute=0, hour='7,12,17,21'),
        'args': (1,),
    },
}
