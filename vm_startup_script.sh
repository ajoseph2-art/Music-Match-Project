#!/bin/bash
set -euxo pipefail
# Configure these settings.
REGION="us-west1"
GCP_PROJECT_ID="big-synthesizer-477321-q1"
ARTIFACT_REPOSITORY_NAME="final"
DOCKER_IMAGE_NAME="final"
DOCKER_IMAGE_TAG="latest"
REG_HOST="${REGION}-docker.pkg.dev"
DOCKER_IMAGE="${REG_HOST}/${GCP_PROJECT_ID}/${ARTIFACT_REPOSITORY_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"

# Docker needs a writable config on COS
export DOCKER_CONFIG=/var/lib/docker-config
mkdir -p "${DOCKER_CONFIG}"

# Get an access token from the instance metadata server
TOKEN="$(curl -s -H 'Metadata-Flavor: Google' \
http://metadata/computeMetadata/v1/instance/service-accounts/default/token \
| awk -F'"' '/access_token/ {print $4}')"

# Authenticate Docker to Artifact Registry
echo "${TOKEN}" | docker login -u oauth2accesstoken --password-stdin "https://${REG_HOST}"

# Pull and run container
docker pull "${DOCKER_IMAGE}"
docker rm -f ${DOCKER_IMAGE_NAME} || true
docker run -d --name ${DOCKER_IMAGE_NAME} --restart=always -p 80:80 "${DOCKER_IMAGE}"

