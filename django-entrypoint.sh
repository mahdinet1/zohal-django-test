#!/bin/sh

if [ "$WAIT_FOR_REDIS" = "true" ]; then
  echo "Waiting for Redis..."
  while ! nc -z redis 6379; do sleep 1; done
fi

if [ "$WAIT_FOR_DB" = "true" ]; then
  echo "Waiting for db..."
  while ! nc -z mongodb 5432; do sleep 1; done
fi

exec
exec python manage.py runserver
#gunicorn djangoProject.wsgi --bind 0.0.0.0:8010 --workers 4 --threads 4

