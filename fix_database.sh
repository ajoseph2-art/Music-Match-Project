#!/bin/bash
# Quick fix script to run migrations in Docker

echo "=== Fixing Database Migrations ==="

# Check if Docker containers are running
if ! docker ps | grep -q musicmatch; then
    echo "Error: Docker containers don't seem to be running."
    echo "Please run: docker compose up -d"
    exit 1
fi

echo "1. Stopping containers..."
docker compose down

echo "2. Removing old database volume (optional - this will delete data)..."
read -p "Do you want to reset the database? This will DELETE all data (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker volume rm "serverside final project_postgres_data" 2>/dev/null || echo "Volume doesn't exist or couldn't be removed"
fi

echo "3. Starting containers..."
docker compose up -d --build

echo "4. Waiting for database to be ready..."
sleep 5

echo "5. Running migrations..."
docker compose exec web python manage.py migrate

echo "6. Verifying migrations..."
docker compose exec web python manage.py showmigrations accounts

echo ""
echo "=== Done ==="
echo "Check the output above. If migrations show [X], they're applied."
echo "If you see [ ], run: docker compose exec web python manage.py migrate"

