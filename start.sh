#!/bin/sh

redis-server &
python -m celery -A config.celery worker --loglevel=info &
python manage.py runserver 0:8000
