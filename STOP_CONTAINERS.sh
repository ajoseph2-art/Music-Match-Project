#!/bin/bash
# Stop all running containers (useful for cleanup)

echo "Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null || echo "No containers to stop"

echo "Removing stopped containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "No containers to remove"

echo "Done!"

