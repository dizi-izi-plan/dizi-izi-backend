#!/bin/sh

echo "----------Apply database migrations----------"
python manage.py migrate --noinput

echo "----------Collect backend Static----------"
python manage.py collectstatic

echo "----------Starting Gunicorn----------"
exec gunicorn config.wsgi:application --bind 0:8000 --workers 3
