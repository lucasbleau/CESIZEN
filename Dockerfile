# Stage build
FROM python:3.12-slim AS build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY cesizen_backend/requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# Stage runtime
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=build /wheels /wheels
COPY --from=build /app/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir /wheels/*

COPY . .

RUN python cesizen_backend/manage.py collectstatic --noinput || true

EXPOSE 8000

ENV PYTHONPATH=/app/cesizen_backend

CMD ["gunicorn","cesizen_backend.wsgi:application","--chdir","cesizen_backend","--bind","0.0.0.0:8000","--workers","3"]