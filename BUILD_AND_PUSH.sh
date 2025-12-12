#!/bin/bash
# Quick script to build and push Docker image to Artifact Registry

set -e

# Configuration
PROJECT_ID="big-synthesizer-477321-q1"
REGION="us-west1"
ARTIFACT_REPOSITORY_NAME="final"
DOCKER_IMAGE_NAME="final"
DOCKER_IMAGE_TAG="latest"

REG_HOST="${REGION}-docker.pkg.dev"
DOCKER_IMAGE="${REG_HOST}/${PROJECT_ID}/${ARTIFACT_REPOSITORY_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"

echo "🐳 Building Docker image for linux/amd64: ${DOCKER_IMAGE}"
docker build --platform linux/amd64 -t "${DOCKER_IMAGE}" .

echo "🔐 Configuring Docker authentication..."
gcloud auth configure-docker ${REG_HOST} --quiet

echo "📤 Pushing to Artifact Registry..."
docker push "${DOCKER_IMAGE}"

echo "✅ Image pushed successfully!"
echo "📍 Image location: ${DOCKER_IMAGE}"
echo ""
echo "📝 To test locally (use SQLite, skip nginx):"
echo "  docker run -it -p 8000:8000 -e USE_SQLITE=True -e DEBUG=True ${DOCKER_IMAGE}"
echo ""
echo "🌐 Then access at: http://localhost:8000"
echo ""
echo "📋 For production deployment:"
echo "  1. Create VM instance in GCP Console"
echo "  2. Use vm_startup_script.sh as startup script"
echo "  3. Access via VM external IP"

