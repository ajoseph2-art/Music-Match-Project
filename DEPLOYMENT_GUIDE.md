# MusicMatch Deployment Guide

## Part 1: Local Testing

### Quick Test (SQLite, no nginx)
```bash
./QUICK_TEST.sh
```
- Access at: http://localhost:8000
- Stop: `docker stop musicmatch_test`

### View Logs
```bash
docker logs -f musicmatch_test
```

---

## Part 2: GCP Deployment

### Step 1: Build & Push Docker Image

```bash
./BUILD_AND_PUSH.sh
```

This builds and pushes to:
`us-west1-docker.pkg.dev/big-synthesizer-477321-q1/final/final:latest`

### Step 2: Create Cloud SQL PostgreSQL Database

1. Go to **GCP Console** → **SQL**
2. Click **Create Instance** → **PostgreSQL**
3. Configure:
   - Instance ID: `musicmatch-db`
   - Password: (save this!)
   - Region: `us-west1`
   - Machine type: `db-f1-micro` (cheapest)
4. Click **Create**
5. Once created, note the **Connection name** (format: `project:region:instance`)

### Step 3: Create the Database

1. In Cloud SQL, click your instance
2. Go to **Databases** tab
3. Click **Create Database**
4. Name: `musicmatch`

### Step 4: Create Instance Template

1. Go to **Compute Engine** → **Instance Templates**
2. Click **Create Instance Template**
3. Configure:
   - Name: `musicmatch-template`
   - Machine type: `e2-micro`
   - Boot disk: **Container-Optimized OS**
   - Firewall: ✅ Allow HTTP traffic
   
4. Expand **Advanced options** → **Management** → **Automation**
5. Paste this startup script (update values):

```bash
#!/bin/bash
set -euxo pipefail

# Configure these settings
REGION="us-west1"
GCP_PROJECT_ID="big-synthesizer-477321-q1"
ARTIFACT_REPOSITORY_NAME="final"
DOCKER_IMAGE_NAME="final"
DOCKER_IMAGE_TAG="latest"

# Database settings
DB_NAME="musicmatch"
DB_USER="postgres"
DB_PASSWORD="YOUR_DB_PASSWORD"
DB_HOST="/cloudsql/big-synthesizer-477321-q1:us-west1:musicmatch-db"

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

# Pull and run
docker pull "${DOCKER_IMAGE}"
docker rm -f musicmatch || true
docker run -d --name musicmatch --restart=always -p 80:80 \
  -e DB_NAME="${DB_NAME}" \
  -e DB_USER="${DB_USER}" \
  -e DB_PASSWORD="${DB_PASSWORD}" \
  -e DB_HOST="${DB_HOST}" \
  -e SECRET_KEY="your-production-secret-key-here" \
  -e DEBUG="False" \
  "${DOCKER_IMAGE}"
```

6. Click **Create**

### Step 5: Create Managed Instance Group

1. Go to **Compute Engine** → **Instance Groups**
2. Click **Create Instance Group**
3. Configure:
   - Name: `musicmatch-group`
   - Instance template: `musicmatch-template`
   - Location: **Multiple zones** (us-west1)
   - Number of instances: `2` (minimum required)
   - Health check: Create new
     - Name: `musicmatch-health-check`
     - Protocol: HTTP
     - Port: `80`
     - Request path: `/`
     - **Check interval**: `10 seconds` (prevents too frequent checks)
     - **Timeout**: `5 seconds`
     - **Healthy threshold**: `2` consecutive successes
     - **Unhealthy threshold**: `3` consecutive failures (prevents premature replacement)
4. Click **Create**

> ⚠️ **Important**: Using check interval ≥10s and unhealthy threshold ≥3 prevents instances from being replaced too often during temporary slowdowns or startup.

### Step 6: Create Load Balancer

1. Go to **Network Services** → **Load Balancing**
2. Click **Create Load Balancer**
3. Choose **HTTP(S) Load Balancing** → **Start Configuration**
4. Select **From Internet to my VMs**
5. Configure:

**Backend:**
- Click **Backend configuration** → **Create backend service**
- Name: `musicmatch-backend`
- Backend type: Instance group
- Instance group: `musicmatch-group`
- Port: `80`
- Health check: Use existing `musicmatch-health-check` or create new:
  - Protocol: HTTP
  - Port: `80`
  - Request path: `/`
  - Check interval: `10 seconds`
  - Unhealthy threshold: `3`
- Click **Create**

**Frontend:**
- Click **Frontend configuration**
- Name: `musicmatch-frontend`
- Protocol: HTTP (initially, add HTTPS later)
- Port: `80`
- Click **Done**

6. Click **Create**
7. **Note the Load Balancer IP address** (e.g., `34.123.45.67`)

---

## Deployment Options

### Option A: Deploy Without Domain (IP Address Only) ✅ Recommended for Testing

#### Step 7A: Update CSRF Settings for IP Address

1. Edit `musicmatch/settings.py` and update `CSRF_TRUSTED_ORIGINS`:
```python
CSRF_TRUSTED_ORIGINS = [
    f'http://{os.getenv("LOAD_BALANCER_IP", "YOUR_LOAD_BALANCER_IP")}',
    # Replace YOUR_LOAD_BALANCER_IP with your actual IP, e.g.:
    'http://34.123.45.67',
]
```

2. Rebuild and push:
```bash
./BUILD_AND_PUSH.sh
```

3. **Access your app**: `http://YOUR_LOAD_BALANCER_IP`
   - Example: `http://34.123.45.67`

4. **Done!** ✅ Your app is live at the IP address.

---

### Option B: Deploy With Domain & SSL (Optional)

#### Step 7B: Register Domain & SSL

1. Register a domain (Namecheap, Google Domains, etc.)
2. Point domain A record to Load Balancer IP
3. In Load Balancer, add HTTPS frontend:
   - Protocol: HTTPS
   - Create Google-managed SSL certificate
   - Add your domain

#### Step 8B: Update CSRF Settings for Domain

In `musicmatch/settings.py`, add your domain:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
    'http://YOUR_LOAD_BALANCER_IP',
]
```

Rebuild and push:
```bash
./BUILD_AND_PUSH.sh
```

---

### Step 9: Restart VMs (Both Options)

To pick up new image:
1. Go to **Instance Groups** → `musicmatch-group`
2. Click **Rolling Restart/Replace**
3. Or manually stop/start VMs

---

## Verification Checklist

- [ ] http://localhost:8000 works locally
- [ ] http://YOUR_VM_IP works (single VM test)
- [ ] http://YOUR_LOAD_BALANCER_IP works
- [ ] https://yourdomain.com works
- [ ] `/server_info/` returns server data
- [ ] Join/Login/Logout works
- [ ] All features functional

---

## Useful Commands

```bash
# View running containers
docker ps

# View container logs
docker logs -f musicmatch_test

# Stop all containers
./STOP_CONTAINERS.sh

# SSH into GCP VM
gcloud compute ssh INSTANCE_NAME --zone=us-west1-a

# View VM startup logs (from inside VM)
sudo journalctl -u google-startup-scripts.service

# Restart instance group
gcloud compute instance-groups managed rolling-action restart \
  musicmatch-group --zone=us-west1-a
```

---

## Quick Reference

| Item | Value |
|------|-------|
| Project ID | `big-synthesizer-477321-q1` |
| Region | `us-west1` |
| Image | `us-west1-docker.pkg.dev/big-synthesizer-477321-q1/final/final:latest` |
| Local test port | `8000` |
| Production port | `80` (nginx) |
