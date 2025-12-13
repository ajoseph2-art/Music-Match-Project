#!/bin/bash
# Build and deploy using Google Cloud Build (no local Docker needed!)

set -e

PROJECT_ID="big-synthesizer-477321-q1"
REGION="us-west1"
ARTIFACT_REPOSITORY_NAME="final"
DOCKER_IMAGE_NAME="final"

REG_HOST="${REGION}-docker.pkg.dev"
DOCKER_IMAGE="${REG_HOST}/${PROJECT_ID}/${ARTIFACT_REPOSITORY_NAME}/${DOCKER_IMAGE_NAME}:latest"

echo "🚀 Building with Google Cloud Build..."
echo "   (No local Docker needed!)"
echo ""

# Submit build to Cloud Build
gcloud builds submit \
    --project=$PROJECT_ID \
    --tag="${DOCKER_IMAGE}" \
    .

echo ""
echo "✅ Image built and pushed to: ${DOCKER_IMAGE}"
echo ""
echo "📋 Next: Create a VM in GCP Console with vm_startup_script.sh"

