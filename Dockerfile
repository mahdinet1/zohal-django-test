FROM python:3.10-alpine
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn
COPY . /app/
RUN pip install -r req.txt

RUN #chmod +x /app/django-entrypoint.sh

