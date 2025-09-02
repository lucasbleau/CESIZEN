FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY cesizen_backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/cesizen_backend

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn","cesizen_backend.wsgi:application","--bind","0.0.0.0:8000"]