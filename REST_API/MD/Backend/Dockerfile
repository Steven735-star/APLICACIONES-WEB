FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev libffi-dev libjpeg-dev zlib1g-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install \
    Django==5.1.4 \
    psycopg2-binary==2.9.10 \
    djangorestframework==3.15.2 \
    djangorestframework-simplejwt==5.3.1 \
    django-filter==24.3 \
    channels==4.1.0 \
    channels-redis==4.2.0 \
    daphne==4.1.2 \
    celery==5.4.0 \
    django-celery-beat==2.7.0 \
    django-celery-results==2.5.1 \
    redis==5.2.1 \
    django-redis==5.4.0 \
    django-fsm==3.0.1 \
    django-auditlog==3.0.0 \
    django-cors-headers==4.6.0 \
    python-decouple==3.8 \
    Pillow==11.0.0 \
    django-debug-toolbar==4.4.6 \
    django-extensions==3.2.3 \
    pytest==8.3.4 \
    pytest-django==4.9.0 \
    pytest-django==4.9.0 \
    whitenoise==6.8.2\
    drf-spectacular==0.28.0

COPY . .

RUN mkdir -p staticfiles media logs

EXPOSE 8000
