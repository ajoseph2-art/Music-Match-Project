#!/bin/bash
# Quick local test script for Docker image

set -e

# Configuration
PROJECT_ID="big-synthesizer-477321-q1"
REGION="us-west1"
ARTIFACT_REPOSITORY_NAME="final"
DOCKER_IMAGE_NAME="final"
DOCKER_IMAGE_TAG="latest"

REG_HOST="${REGION}-docker.pkg.dev"
DOCKER_IMAGE="${REG_HOST}/${PROJECT_ID}/${ARTIFACT_REPOSITORY_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"

echo "🧪 Testing Docker image locally..."
echo "📍 Image: ${DOCKER_IMAGE}"
echo ""

# Stop any existing containers using port 8000
echo "Checking for existing containers on port 8000..."
EXISTING=$(docker ps -q --filter "publish=8000" 2>/dev/null || echo "")
if [ ! -z "$EXISTING" ]; then
    echo "Stopping existing container(s) on port 8000..."
    docker stop $EXISTING 2>/dev/null || true
    docker rm $EXISTING 2>/dev/null || true
fi

echo "Using SQLite (no PostgreSQL needed)"
echo "Skipping nginx (port 80 conflict)"
echo ""

# Run in detached mode
CONTAINER_ID=$(docker run -d --rm -p 8000:8000 \
  --name musicmatch_test \
  -e USE_SQLITE=True \
  -e DEBUG=True \
  "${DOCKER_IMAGE}")

echo "✅ Container started: ${CONTAINER_ID:0:12}"
echo ""
echo "🌐 Access at: http://localhost:8000"
echo ""
echo "📋 View logs: docker logs -f musicmatch_test"
echo "🛑 Stop:      docker stop musicmatch_test"
echo ""

# Wait a moment then show initial logs
sleep 3
echo "=== Container Logs ==="
docker logs musicmatch_test 2>&1 | tail -20

