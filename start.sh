#!/bin/bash

# Set USE_SQLITE if not provided (for local testing)
if [ -z "$USE_SQLITE" ]; then
    export USE_SQLITE="False"
fi

# Start Cloud SQL Proxy if DB_HOST is a connection name (contains colons) and not using SQLite
if [ "${USE_SQLITE}" != "True" ] && [[ "$DB_HOST" == *":"* ]] && [[ "$DB_HOST" == *"/cloudsql/"* ]]; then
    echo "Starting Cloud SQL Proxy for $DB_HOST..."
    /app/cloud_sql_proxy -instances=${DB_HOST#/cloudsql/}=tcp:5432 &
    sleep 5
    export DB_HOST=127.0.0.1
    echo "Cloud SQL Proxy started, DB_HOST set to 127.0.0.1"
fi

# Run migrations (will use SQLite if USE_SQLITE=True)
echo "Running database migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Calculate worker processes: 2 * CPU_COUNT + 1
CPU_COUNT=$(nproc)
WORKERS=$((2 * CPU_COUNT + 1))
echo "CPU count: $CPU_COUNT, Gunicorn workers: $WORKERS"

# If SKIP_NGINX=True (local dev only), run gunicorn only on 8000
# Note: USE_SQLITE alone should NOT skip nginx - SQLite can run in production with nginx
if [ "${SKIP_NGINX}" = "True" ] || [ "${SKIP_NGINX}" = "true" ]; then
    echo "Starting gunicorn only (dev mode - no nginx)..."
    exec gunicorn --bind 0.0.0.0:8000 --workers $WORKERS musicmatch.wsgi:application
fi

# Otherwise, production: run gunicorn then nginx
echo "Starting gunicorn with $WORKERS workers..."
gunicorn --bind 0.0.0.0:8000 --workers $WORKERS musicmatch.wsgi:application &

echo "Starting nginx..."
echo "MusicMatch is ready!"
nginx -g "daemon off;"
