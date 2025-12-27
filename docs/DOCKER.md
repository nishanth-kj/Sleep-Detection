# 🐳 Docker Setup Guide

## Issues Fixed

✅ Removed obsolete `version: '3.8'` field (Docker Compose v2 doesn't need it)
✅ Disabled backend services (api/ directory is empty)
✅ Configured for frontend-only deployment

---

## 🚨 Current Issue

**Docker Desktop is NOT running!**

The error you're seeing indicates the Docker daemon isn't started:
```
The system cannot find the file specified: //./pipe/dockerDesktopLinuxEngine
```

---

## 🔧 How to Fix

### Step 1: Start Docker Desktop

1. **Open Docker Desktop** from Windows Start Menu
2. Wait for Docker to fully start (whale icon in system tray should be stable)
3. Verify Docker is running:
   ```powershell
   docker --version
   docker ps
   ```

### Step 2: Run Docker Compose

Once Docker Desktop is running, execute:

```powershell
cd C:\Projects\Sleep-Detection
docker compose up -d --build
```

This will:
- Build the Next.js web app container
- Start it in detached mode
- Expose it on http://localhost:80

---

## 🎯 What Will Run

Currently, only the **frontend service** is configured:

```yaml
services:
  frontend:
    build: ./web
    ports: "80:3000"
    environment: NODE_ENV=production
```

**Access at:** http://localhost:80

---

## 📝 Backend (Future)

The backend services are commented out because `api/` is empty. To enable them:

1. Restore the Python backend files to `api/`
2. Uncomment backend sections in `docker-compose.yml`
3. Rebuild: `docker compose up -d --build`

---

## 🛠️ Useful Docker Commands

```powershell
# Check if Docker is running
docker info

# View running containers
docker ps

# View logs
docker compose logs -f

# Stop containers
docker compose down

# Rebuild and restart
docker compose up -d --build

# Remove all containers and images
docker compose down --rmi all
```

---

## ⚡ Alternative: Run Without Docker

If Docker continues to have issues, you can run the web app directly:

```powershell
cd web
npm install
npm run dev
```

**Access at:** http://localhost:3000

This works perfectly and doesn't require Docker!

---

## 🔍 Troubleshooting

### Docker Desktop won't start
- Check Windows Services → Docker Desktop Service should be "Running"
- Try restarting: Right-click Docker Desktop → Quit → Start again
- Ensure WSL 2 is installed (required for Docker Desktop on Windows)

### Build fails
- Clear Docker cache: `docker system prune -a`
- Delete `web/.next` folder: `Remove-Item -Recurse -Force web\.next`
- Rebuild: `docker compose up -d --build`

### Port conflict
- Change port in docker-compose.yml: `"8080:3000"` instead of `"80:3000"`

---

**Recommendation:** Since the web app is already running on `npm run dev`, you don't need Docker unless you want containerized deployment.
