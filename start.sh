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

# Wait for database to be ready (if using PostgreSQL)
if [ "${USE_SQLITE}" != "True" ]; then
    echo "Waiting for PostgreSQL to be ready..."
    max_attempts=30
    attempt=1
    while [ $attempt -le $max_attempts ]; do
        # Try to connect to PostgreSQL
        PGPASSWORD="${DB_PASSWORD}" psql -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" -c "SELECT 1;" >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "PostgreSQL is ready!"
            break
        fi
        echo "Waiting for database... attempt $attempt/$max_attempts"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        echo "ERROR: Could not connect to PostgreSQL after $max_attempts attempts"
        echo "Attempting to continue anyway..."
    fi
fi

# Run migrations (will use SQLite if USE_SQLITE=True)
echo "Running database migrations..."
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "ERROR: Migration failed!"
    exit 1
fi
echo "Migrations completed successfully."

# Verify key tables exist
echo "Verifying database tables..."
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
try:
    if '${USE_SQLITE}' == 'True':
        cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name='accounts_userprofile'\")
    else:
        cursor.execute(\"SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename='accounts_userprofile'\")
    result = cursor.fetchone()
    if result:
        print('✓ accounts_userprofile table exists')
    else:
        print('✗ ERROR: accounts_userprofile table does not exist!')
        exit(1)
except Exception as e:
    print(f'Error checking tables: {e}')
    exit(1)
"
if [ $? -ne 0 ]; then
    echo "ERROR: Database verification failed!"
    exit 1
fi

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
