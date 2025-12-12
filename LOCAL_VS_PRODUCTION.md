# Local Testing vs Production Deployment

## Local Testing (Your Machine)

### Problem: Port 80 is already in use
Your local machine likely has something running on port 80 (Apache, nginx, etc.)

### Solution: Use SQLite and skip nginx

```bash
# Quick test script
./QUICK_TEST.sh

# Or manually:
docker run -it -p 8000:8000 \
  -e USE_SQLITE=True \
  -e DEBUG=True \
  us-west1-docker.pkg.dev/big-synthesizer-477321-q1/final/final:latest
```

**Access at**: http://localhost:8000

**What happens**:
- ✅ Uses SQLite (no PostgreSQL needed)
- ✅ Skips nginx (avoids port 80 conflict)
- ✅ Runs gunicorn on port 8000
- ✅ DEBUG mode enabled

## Production Deployment (GCP VM)

### On GCP, port 80 is available

**VM Startup Script** (`vm_startup_script.sh`):
- ✅ Pulls image from Artifact Registry
- ✅ Runs with nginx + gunicorn
- ✅ Listens on port 80
- ✅ Uses PostgreSQL (via Cloud SQL)

**Access at**: `http://<VM_EXTERNAL_IP>`

## Summary

| Environment | Database | Web Server | Port | Command |
|------------|----------|------------|------|---------|
| **Local** | SQLite | Gunicorn only | 8000 | `./QUICK_TEST.sh` |
| **Production** | PostgreSQL | nginx + Gunicorn | 80 | VM startup script |

## Quick Commands

### Build and Push
```bash
./BUILD_AND_PUSH.sh
```

### Test Locally
```bash
./QUICK_TEST.sh
```

### Deploy to GCP
1. Use `vm_startup_script.sh` in VM instance startup script
2. Wait for VM to start
3. Access via VM external IP

