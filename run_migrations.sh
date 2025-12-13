#!/bin/bash
# Simple script to run migrations in Docker

echo "Running database migrations in Docker container..."
echo ""
echo "If you see an error, make sure Docker containers are running first:"
echo "  docker compose up -d"
echo ""

# Try docker compose (newer syntax)
if command -v docker &> /dev/null; then
    if docker compose version &> /dev/null 2>&1; then
        docker compose exec web python manage.py migrate
        echo ""
        echo "Migration complete! Login should work now."
        exit 0
    fi
fi

# Try docker-compose (older syntax)
if command -v docker-compose &> /dev/null; then
    docker-compose exec web python manage.py migrate
    echo ""
    echo "Migration complete! Login should work now."
    exit 0
fi

echo "ERROR: Docker not found. Please run migrations manually:"
echo "  docker compose exec web python manage.py migrate"

