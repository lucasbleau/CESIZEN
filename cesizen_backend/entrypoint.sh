#!/bin/sh
set -e
echo "[entrypoint] Waiting DB..."
python - <<'PY'
import time,os,sys,psycopg2
url=os.getenv("DATABASE_URL")
for i in range(40):
    try:
        psycopg2.connect(url); break
    except Exception:
        time.sleep(1)
else:
    print("DB not reachable", file=sys.stderr); sys.exit(1)
PY
echo "[entrypoint] Migrate"
python manage.py migrate --noinput
echo "[entrypoint] Run gunicorn"
exec gunicorn cesizen_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3