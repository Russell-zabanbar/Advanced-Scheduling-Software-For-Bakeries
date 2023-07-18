FROM python:3.11.4-bullseye

WORKDIR /src


COPY requirements.txt /src/
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /src/

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=mapi.settings

CMD gunicorn mapi.wsgi :8000 & celery -A mapi worker -l INFO & celery -A mapi beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler


