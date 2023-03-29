import os
import time

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoworld.settings')

app = Celery('autoworld')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def debug_task():
    time.sleep(5)
    print('Hello from CELERY')
    # return 'Hello from CELERY'

# from autoworld.celery import debug_task