#!/bin/sh

python manage.py runserver 0:8000 &
python -m celery -A config.celery worker --loglevel=info
