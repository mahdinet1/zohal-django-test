echo "Starting Celery Worker..."
exec celery -A djangoProject worker --loglevel=info