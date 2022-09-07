#!/bin/bash
python manage.py rename_app food foods
python manage.py makemigrations foods users
python manage.py migrate 
python manage.py collectstatic --no-input
python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USER \
        --email $DJANGO_SUPERUSER_EMAIL
# exec gunicorn foodgram.wsgi:application --bind 0:8000
exec python3 manage.py runserver 0:8000