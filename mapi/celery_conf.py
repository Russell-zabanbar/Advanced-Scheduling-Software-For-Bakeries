import os
from celery import Celery
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mapi.settings')

app = Celery('mapi')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_url = 'amqp://guest:guest@localhost'
app.conf.result_backend = 'django-db'
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json', 'pickle']






