#!/bin/bash
python manage.py makemigrations foods users
python manage.py migrate 
python manage.py collectstatic --no-input
python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USER \
        --email $DJANGO_SUPERUSER_EMAIL
exec gunicorn foodgram.wsgi:application --bind 0:8000
