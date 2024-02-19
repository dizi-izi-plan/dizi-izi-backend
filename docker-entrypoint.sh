#!/bin/sh

echo "----------Collect static files----------"
python manage.py collectstatic --noinput

echo "----------Make migrations----------"
python manage.py makemigrations

echo "----------Apply database migrations----------"
python manage.py migrate --noinput

echo "----------Starting Gunicorn----------"
exec gunicorn config.wsgi:application --bind 0:8000 --workers 3
