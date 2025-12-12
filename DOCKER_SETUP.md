# Docker Setup for macOS

## Docker Desktop is Installed

Docker Desktop is installed in `/Applications/Docker.app` but needs to be running.

## Start Docker Desktop

### Option 1: From Terminal
```bash
open -a Docker
```

### Option 2: From Applications
1. Open Finder
2. Go to Applications
3. Double-click "Docker"
4. Wait for Docker to start (whale icon in menu bar)

## Verify Docker is Running

After starting Docker Desktop, wait 30-60 seconds, then check:

```bash
docker --version
docker ps
```

You should see Docker version and an empty container list.

## If Docker Still Not Found

Add Docker to your PATH by adding this to `~/.zshrc`:

```bash
# Add Docker to PATH
export PATH="/usr/local/bin:$PATH"
```

Then reload:
```bash
source ~/.zshrc
```

## Alternative: Use Docker via Colima (Lightweight)

If Docker Desktop is too heavy, you can use Colima:

```bash
# Install via Homebrew
brew install colima docker docker-compose

# Start Colima
colima start

# Verify
docker --version
```

## For GCP Deployment

Once Docker is running, you can:

1. Build your image:
   ```bash
   docker build -t gcr.io/PROJECT_ID/musicmatch:latest .
   ```

2. Push to GCR:
   ```bash
   docker push gcr.io/PROJECT_ID/musicmatch:latest
   ```

3. Or run the deployment script:
   ```bash
   ./QUICK_DEPLOY.sh
   ```

