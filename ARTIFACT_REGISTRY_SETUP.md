# Artifact Registry Setup Guide

## Your Project Configuration

- **Region**: `us-west1`
- **GCP Project ID**: `big-synthesizer-477321-q1`
- **Artifact Repository Name**: `final`
- **Docker Image Name**: `final`
- **Full Image Name**: `us-west1-docker.pkg.dev/big-synthesizer-477321-q1/final/final:latest`

## Step 1: Install GCP SDK (if not already installed)

```bash
cd /workspaces
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xzf google-cloud-cli-linux-x86_64.tar.gz
cd google-cloud-sdk
./install.sh
# Accept all defaults
```

## Step 2: Initialize and Authenticate

```bash
# Open a new terminal window
gcloud init
# Complete authentication steps
# You don't need to select a default region

# Configure Docker for Artifact Registry
gcloud auth configure-docker us-west1-docker.pkg.dev
```

## Step 3: Enable Artifact Registry API

1. Login to GCP: https://console.cloud.google.com/
2. Pin "Artifact Registry" to main navigation menu
3. Navigate to Artifact Registry
4. Select "Enable Artifact Registry API"
5. Navigate to Artifact Registry > Repositories
6. Create new Repository:
   - **Name**: `final` (must be all lower-case)
   - **Format**: Docker
   - **Mode**: Standard
   - **Location Type**: Region
   - **Region**: `us-west1`
   - Leave all other options as default
   - Select "Create" button

## Step 4: Build and Push Docker Image

```bash
# Build with Artifact Registry naming convention
docker build -t us-west1-docker.pkg.dev/big-synthesizer-477321-q1/final/final:latest .

# Test locally (optional)
docker run -it -p 8000:8000 \
  -e USE_SQLITE=True \
  -e DEBUG=True \
  us-west1-docker.pkg.dev/big-synthesizer-477321-q1/final/final:latest

# Authenticate (if needed)
gcloud auth login

# Push to Artifact Registry
docker push us-west1-docker.pkg.dev/big-synthesizer-477321-q1/final/final:latest
```

## Step 5: Verify Image in Artifact Registry

1. GCP Main Navigation Menu > Artifact Registry
2. You should see the image under the `final` repository

## Step 6: Create VM Instance with Startup Script

1. GCP Main Navigation Menu > Compute Engine > VM Instances
2. Select "Create Instance"
3. Configure:
   - **Name**: `musicmatch-instance` (or your preferred name)
   - **Region**: `us-west1`
   - **Zone**: Leave default
   - **Machine type**: `e2-micro` (2 vCPU, 1 GB memory)
   - **Boot disk**: Container Optimized OS
   - **Firewall**: Allow HTTP traffic
4. Expand "Advanced" section
5. Under "Automation" > "Startup script", paste the contents of `vm_startup_script.sh`
6. Click "Create"

## Step 7: Verify Deployment

After VM starts (may take several minutes):

1. **View startup logs** in GCP console (VM instance > View logs)
2. **SSH into VM**:
   ```bash
   gcloud compute ssh musicmatch-instance --zone=us-west1-a
   ```
3. **Check Docker container**:
   ```bash
   docker ps
   docker logs -f <container_id>
   ```
4. **Access your app**: `http://<VM_EXTERNAL_IP>`

## Troubleshooting

### View VM Startup Logs
- GCP Console > Compute Engine > VM Instances > Your Instance > "View logs"

### SSH into VM
```bash
# Method 1: Browser SSH button in GCP console
# Method 2: CLI with gcloud
gcloud compute ssh instance-name --zone=us-west1-a

# Method 3: Direct SSH
ssh username@<VM_IP_ADDRESS>
```

### View Docker Container Logs
```bash
# Inside the VM
docker ps  # Note container ID
docker logs -f <container_id>
```

### Common Issues

**Image not found**: Make sure you've pushed the image to Artifact Registry
**Authentication failed**: Run `gcloud auth configure-docker us-west1-docker.pkg.dev`
**Container not starting**: Check startup logs in GCP console
**Port 80 not accessible**: Ensure firewall rule allows HTTP traffic

## Quick Reference

**Image Name Format**:
```
<region>-docker.pkg.dev/<gcp-project-ID>/<artifact-repository-name>/<docker-image-name>:<docker-image-tag>
```

**Your Image**:
```
us-west1-docker.pkg.dev/big-synthesizer-477321-q1/final/final:latest
```

**Build Command**:
```bash
docker build -t us-west1-docker.pkg.dev/big-synthesizer-477321-q1/final/final:latest .
```

**Push Command**:
```bash
docker push us-west1-docker.pkg.dev/big-synthesizer-477321-q1/final/final:latest
```

