echo "Starting Celery Beat..."
exec celery -A djangoProject beat --loglevel=info