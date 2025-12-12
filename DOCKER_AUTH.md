# Docker Authentication for GCP

## For Google Container Registry (GCR) - Used in this project

```bash
gcloud auth configure-docker
```

This configures Docker to authenticate with `gcr.io` automatically.

## For Artifact Registry (Alternative)

If you're using Artifact Registry instead of GCR:

```bash
# Replace REGION with your region (e.g., us-west1)
gcloud auth configure-docker REGION-docker.pkg.dev
```

Example:
```bash
gcloud auth configure-docker us-west1-docker.pkg.dev
```

## Verify Authentication

After running the command, test it:

```bash
# For GCR
docker pull gcr.io/PROJECT_ID/musicmatch:latest

# For Artifact Registry
docker pull REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/musicmatch:latest
```

## Common Issues

**Error: "no such file or directory"**
- Don't use `<` or `>` characters
- Use the command exactly as shown above

**Error: "permission denied"**
- Make sure you're logged in: `gcloud auth login`
- Verify your project: `gcloud config get-value project`

## Quick Fix

If you're following the QUICK_DEPLOY.sh script, just run:

```bash
gcloud auth configure-docker
```

This is already included in the script and will work for GCR.

