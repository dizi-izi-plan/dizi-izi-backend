#!/bin/sh

echo "----------Apply database migrations----------"
python manage.py migrate --noinput

echo "----------Compilation of translation binary file ----------"
python manage.py compilemessages

echo "----------Starting Gunicorn----------"
exec gunicorn config.wsgi:application --bind 0:8000 --workers 3
