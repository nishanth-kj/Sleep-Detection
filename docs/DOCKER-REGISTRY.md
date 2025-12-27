# Docker Registry Guide

This guide explains how to push your Sleep Detection Docker images to GitHub Container Registry (GHCR) or Docker Hub.

## Option 1: GitHub Container Registry (GHCR) - Recommended

### Automatic Publishing via GitHub Actions

The project includes a GitHub Actions workflow that automatically builds and publishes images when you push to the main branch.

**What happens automatically:**
- On every push to `main`/`master`: Images are built and pushed to GHCR
- On version tags (e.g., `v1.0.0`): Images are tagged with the version number
- Images are available at: `ghcr.io/<your-username>/sleep-detection-frontend` and `ghcr.io/<your-username>/sleep-detection-backend`

### Manual Push to GHCR

1. **Login to GitHub Container Registry:**
   ```bash
   # Create a Personal Access Token (PAT) with 'write:packages' permission
   # Go to: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   
   echo YOUR_GITHUB_PAT | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
   ```

2. **Tag your images:**
   ```bash
   # Replace <username> with your GitHub username
   docker tag sleep-detection-frontend ghcr.io/<username>/sleep-detection-frontend:latest
   docker tag sleep-detection-backend ghcr.io/<username>/sleep-detection-backend:latest
   docker tag sleep-detection-mlflow_ui ghcr.io/<username>/sleep-detection-mlflow-ui:latest
   ```

3. **Push to GHCR:**
   ```bash
   docker push ghcr.io/<username>/sleep-detection-frontend:latest
   docker push ghcr.io/<username>/sleep-detection-backend:latest
   docker push ghcr.io/<username>/sleep-detection-mlflow-ui:latest
   ```

4. **Make packages public (optional):**
   - Go to your GitHub profile → Packages
   - Select the package → Package settings
   - Change visibility to Public

## Option 2: Docker Hub

### Manual Push to Docker Hub

1. **Login to Docker Hub:**
   ```bash
   docker login
   # Enter your Docker Hub username and password
   ```

2. **Tag your images:**
   ```bash
   # Replace <username> with your Docker Hub username
   docker tag sleep-detection-frontend <username>/sleep-detection-frontend:latest
   docker tag sleep-detection-backend <username>/sleep-detection-backend:latest
   docker tag sleep-detection-mlflow_ui <username>/sleep-detection-mlflow-ui:latest
   ```

3. **Push to Docker Hub:**
   ```bash
   docker push <username>/sleep-detection-frontend:latest
   docker push <username>/sleep-detection-backend:latest
   docker push <username>/sleep-detection-mlflow-ui:latest
   ```

## Using Published Images

Once published, update your `docker-compose.yml` to use the published images:

```yaml
services:
  frontend:
    image: ghcr.io/<username>/sleep-detection-frontend:latest
    # Remove the 'build' section
    ports:
      - "80:3000"
    # ... rest of config

  backend:
    image: ghcr.io/<username>/sleep-detection-backend:latest
    # Remove the 'build' section
    ports:
      - "8000:8000"
    # ... rest of config

  mlflow_ui:
    image: ghcr.io/<username>/sleep-detection-backend:latest
    # Uses same image as backend
    command: mlflow ui --backend-store-uri postgresql://sleepsafe:sleepsafe_password@postgres:5432/sleepsafe --host 0.0.0.0 --port 5000
    # ... rest of config
```

## Version Tagging

For production deployments, use version tags:

```bash
# Tag a specific version
docker tag sleep-detection-frontend ghcr.io/<username>/sleep-detection-frontend:v1.0.0
docker push ghcr.io/<username>/sleep-detection-frontend:v1.0.0

# Also push as latest
docker push ghcr.io/<username>/sleep-detection-frontend:latest
```

## Quick Commands Reference

```powershell
# Build all images locally
docker compose build

# Tag all images for GHCR (replace <username>)
docker tag sleep-detection-frontend ghcr.io/<username>/sleep-detection-frontend:latest
docker tag sleep-detection-backend ghcr.io/<username>/sleep-detection-backend:latest
docker tag sleep-detection-mlflow_ui ghcr.io/<username>/sleep-detection-mlflow-ui:latest

# Push all to GHCR
docker push ghcr.io/<username>/sleep-detection-frontend:latest
docker push ghcr.io/<username>/sleep-detection-backend:latest
docker push ghcr.io/<username>/sleep-detection-mlflow-ui:latest

# Pull from GHCR
docker pull ghcr.io/<username>/sleep-detection-frontend:latest
docker pull ghcr.io/<username>/sleep-detection-backend:latest
```

## Troubleshooting

### Authentication Issues
- **GHCR**: Ensure your PAT has `write:packages` and `read:packages` permissions
- **Docker Hub**: Verify your Docker Hub credentials

### Package Visibility
- By default, GHCR packages are private
- Go to GitHub → Your Profile → Packages → Package Settings to change visibility

### Rate Limits
- Docker Hub has pull rate limits for free accounts
- GHCR has more generous limits and is recommended for GitHub projects
