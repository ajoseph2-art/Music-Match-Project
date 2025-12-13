#!/bin/bash
# Quick fix: Run migrations in Docker without waiting for full rebuild

echo "Quick Docker Migration Fix"
echo ""

# Check if container is running
CONTAINER=$(docker ps --format "{{.Names}}" | grep -E "web|musicmatch" | head -1)

if [ -z "$CONTAINER" ]; then
    echo "No running container found. Starting containers..."
    docker compose up -d
    echo "Waiting 10 seconds for containers to start..."
    sleep 10
    CONTAINER=$(docker ps --format "{{.Names}}" | grep -E "web|musicmatch" | head -1)
fi

if [ -z "$CONTAINER" ]; then
    echo "ERROR: Could not find or start container"
    echo "Try: docker compose up -d"
    exit 1
fi

echo "Found container: $CONTAINER"
echo "Running migrations..."
docker exec -it "$CONTAINER" python manage.py migrate

echo ""
echo "Done! Login should work now at http://localhost:8000/accounts/login/"

