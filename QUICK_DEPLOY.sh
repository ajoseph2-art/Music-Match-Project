#!/bin/bash
# Quick Deployment Script for MusicMatch to GCP
# Make sure to set your variables before running!

set -e  # Exit on error

# Configuration - UPDATE THESE VALUES
PROJECT_ID="big-synthesizer-477321-q1"
REGION="us-west1"
ZONE="us-west1-a"
DOMAIN="yourdomain.com"
ARTIFACT_REPOSITORY_NAME="final"
DOCKER_IMAGE_NAME="final"
DB_PASSWORD="CHANGE_THIS_SECURE_PASSWORD"
DB_USER_PASSWORD="CHANGE_THIS_TOO"
DJANGO_SECRET_KEY="$(openssl rand -hex 32)"

echo "🚀 Starting MusicMatch Deployment to GCP"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Domain: $DOMAIN"
echo ""

# Step 1: Set project
echo "📋 Setting GCP project..."
gcloud config set project $PROJECT_ID

# Step 2: Enable APIs
echo "🔌 Enabling required APIs..."
gcloud services enable compute.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Step 3: Build and push Docker image to Artifact Registry
echo "🐳 Building Docker image..."
cd "$(dirname "$0")"
REG_HOST="${REGION}-docker.pkg.dev"
DOCKER_IMAGE="${REG_HOST}/${PROJECT_ID}/${ARTIFACT_REPOSITORY_NAME}/${DOCKER_IMAGE_NAME}:latest"
docker build -t "${DOCKER_IMAGE}" .

echo "📤 Pushing Docker image to Artifact Registry..."
gcloud auth configure-docker ${REG_HOST} --quiet
docker push "${DOCKER_IMAGE}"

# Step 4: Create Cloud SQL instance
echo "🗄️  Creating PostgreSQL database..."
gcloud sql instances create musicmatch-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=$REGION \
    --root-password=$DB_PASSWORD \
    --quiet || echo "Database instance may already exist"

echo "📊 Creating database..."
gcloud sql databases create musicmatch --instance=musicmatch-db --quiet || echo "Database may already exist"

echo "👤 Creating database user..."
gcloud sql users create musicmatch_user \
    --instance=musicmatch-db \
    --password=$DB_USER_PASSWORD \
    --quiet || echo "User may already exist"

# Get connection name
CONNECTION_NAME=$(gcloud sql instances describe musicmatch-db --format="value(connectionName)")
echo "Connection name: $CONNECTION_NAME"

# Step 5: Create startup script
echo "📝 Creating startup script..."
cat > startup-script.sh <<EOF
#!/bin/bash
export DB_NAME=musicmatch
export DB_USER=musicmatch_user
export DB_PASSWORD=$DB_USER_PASSWORD
export DB_HOST=/cloudsql/$CONNECTION_NAME
export DB_PORT=5432
export SECRET_KEY=$DJANGO_SECRET_KEY
export DEBUG=False
export USE_SQLITE=False
export ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN

# Download Cloud SQL Proxy
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O /tmp/cloud_sql_proxy
chmod +x /tmp/cloud_sql_proxy

# Start Cloud SQL Proxy
/tmp/cloud_sql_proxy -instances=$CONNECTION_NAME=tcp:5432 &
sleep 5

# Authenticate Docker to Artifact Registry
REG_HOST="${REGION}-docker.pkg.dev"
DOCKER_IMAGE="${REG_HOST}/${PROJECT_ID}/${ARTIFACT_REPOSITORY_NAME}/${DOCKER_IMAGE_NAME}:latest"
TOKEN="\$(curl -s -H 'Metadata-Flavor: Google' \\
http://metadata/computeMetadata/v1/instance/service-accounts/default/token \\
| awk -F'\"' '/access_token/ {print \$4}')"
export DOCKER_CONFIG=/var/lib/docker-config
mkdir -p "\${DOCKER_CONFIG}"
echo "\${TOKEN}" | docker login -u oauth2accesstoken --password-stdin "https://\${REG_HOST}"

# Pull and run Docker container
docker pull "\${DOCKER_IMAGE}"
docker rm -f musicmatch || true
docker run -d \\
    --name musicmatch \\
    --restart=always \\
    -p 80:80 \\
    -e DB_NAME=\$DB_NAME \\
    -e DB_USER=\$DB_USER \\
    -e DB_PASSWORD=\$DB_PASSWORD \\
    -e DB_HOST=127.0.0.1 \\
    -e DB_PORT=\$DB_PORT \\
    -e SECRET_KEY=\$SECRET_KEY \\
    -e DEBUG=\$DEBUG \\
    -e USE_SQLITE=\$USE_SQLITE \\
    -e ALLOWED_HOSTS=\$ALLOWED_HOSTS \\
    "\${DOCKER_IMAGE}"
EOF


# Step 6: Create instance template
echo "📦 Creating instance template..."
gcloud compute instance-templates create musicmatch-template \
    --machine-type=e2-small \
    --image-family=cos-stable \
    --image-project=cos-cloud \
    --boot-disk-size=20GB \
    --tags=http-server,https-server \
    --metadata-from-file startup-script=startup-script.sh \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --quiet || echo "Template may already exist"

# Step 7: Create health check
echo "🏥 Creating health check..."
gcloud compute health-checks create http musicmatch-health-check \
    --port=80 \
    --request-path=/server_info/ \
    --check-interval=10s \
    --timeout=5s \
    --unhealthy-threshold=3 \
    --healthy-threshold=2 \
    --quiet || echo "Health check may already exist"

# Step 8: Create managed instance group
echo "👥 Creating managed instance group..."
gcloud compute instance-groups managed create musicmatch-group \
    --base-instance-name=musicmatch \
    --size=2 \
    --template=musicmatch-template \
    --zone=$ZONE \
    --health-check=musicmatch-health-check \
    --initial-delay=300 \
    --quiet || echo "Instance group may already exist"

# Step 9: Create backend service
echo "🔙 Creating backend service..."
gcloud compute backend-services create musicmatch-backend \
    --protocol=HTTP \
    --health-checks=musicmatch-health-check \
    --global \
    --quiet || echo "Backend service may already exist"

# Add backend
gcloud compute backend-services add-backend musicmatch-backend \
    --instance-group=musicmatch-group \
    --instance-group-zone=$ZONE \
    --global \
    --quiet || echo "Backend may already be added"

# Step 10: Create load balancer
echo "⚖️  Creating load balancer..."
gcloud compute url-maps create musicmatch-map \
    --default-service=musicmatch-backend \
    --quiet || echo "URL map may already exist"

gcloud compute target-http-proxies create musicmatch-http-proxy \
    --url-map=musicmatch-map \
    --quiet || echo "HTTP proxy may already exist"

# Get or create IP
LB_IP=$(gcloud compute addresses describe musicmatch-ip --global --format="value(address)" 2>/dev/null || echo "")
if [ -z "$LB_IP" ]; then
    echo "📍 Creating static IP..."
    gcloud compute addresses create musicmatch-ip --global --quiet
    LB_IP=$(gcloud compute addresses describe musicmatch-ip --global --format="value(address)")
fi

echo "Load Balancer IP: $LB_IP"

gcloud compute forwarding-rules create musicmatch-http-rule \
    --global \
    --target-http-proxy=musicmatch-http-proxy \
    --ports=80 \
    --address=musicmatch-ip \
    --quiet || echo "Forwarding rule may already exist"

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "📋 Next Steps:"
echo "1. Update your DNS A record to point to: $LB_IP"
echo "2. Create SSL certificate:"
echo "   gcloud compute ssl-certificates create musicmatch-ssl-cert \\"
echo "       --domains=$DOMAIN,www.$DOMAIN --global"
echo "3. Create HTTPS proxy and forwarding rule"
echo "4. Wait for instances to be healthy (5-10 minutes)"
echo "5. SSH into an instance and run migrations:"
echo "   gcloud compute ssh musicmatch-XXXX --zone=$ZONE"
echo "   docker exec -it \$(docker ps -q) python manage.py migrate"
echo "   docker exec -it \$(docker ps -q) python manage.py createsuperuser"
echo ""
echo "🔗 Your app will be available at: http://$LB_IP"
echo "🔐 After SSL setup: https://$DOMAIN"

