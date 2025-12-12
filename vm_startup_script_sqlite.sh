#!/bin/bash
set -euxo pipefail

# Configure these settings
REGION="us-west1"
GCP_PROJECT_ID="big-synthesizer-477321-q1"
ARTIFACT_REPOSITORY_NAME="final"
DOCKER_IMAGE_NAME="final"
DOCKER_IMAGE_TAG="latest"

REG_HOST="${REGION}-docker.pkg.dev"
DOCKER_IMAGE="${REG_HOST}/${GCP_PROJECT_ID}/${ARTIFACT_REPOSITORY_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"

# Docker config
export DOCKER_CONFIG=/var/lib/docker-config
mkdir -p "${DOCKER_CONFIG}"

# Get access token
TOKEN="$(curl -s -H 'Metadata-Flavor: Google' \
  http://metadata/computeMetadata/v1/instance/service-accounts/default/token \
  | awk -F'"' '/access_token/ {print $4}')"

# Login to Artifact Registry
echo "${TOKEN}" | docker login -u oauth2accesstoken --password-stdin "https://${REG_HOST}"

# Pull and run container with SQLite
docker pull "${DOCKER_IMAGE}"
docker rm -f musicmatch || true
docker run -d --name musicmatch --restart=always -p 80:80 \
  -e USE_SQLITE=True \
  -e SECRET_KEY="your-production-secret-key-change-this" \
  -e DEBUG=False \
  "${DOCKER_IMAGE}"

