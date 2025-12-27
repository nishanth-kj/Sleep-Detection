# SleepSafe Deployment Guide

## 🚀 Current Status

### ✅ Working Components

- **Web Application (Next.js PWA)**: Fully functional at http://localhost:3000
  - Real-time face detection using MediaPipe
  - TensorFlow.js running with WebGL backend
  - Eye Aspect Ratio (EAR) calculation
  - Audio alarm system
  - Dark/Light mode UI
  - PWA capabilities enabled

### 🏗️ In Progress

- **Backend API**: Directory structure exists but needs Python files restored
- **Mobile Apps**: Skeleton code ready, needs:
  - Rust core compilation for Android (`libsleep_core.so`)
  - Rust core compilation for iOS (`libsleep_core.a`)
  - Integration testing

### 📦 Empty Directories

- `api/` - Backend needs to be restored from git history or recreated
- `lib/npm/` - Future NPM package placeholder
- `lib/pypi/` - Future PyPI package placeholder

---

## 🏃 Running the Project

### Web Application (Recommended)

The web app is the **most complete** component and works standalone:

```bash
cd web
npm install  # Only needed once
npm run dev  # Start development server
```

Visit **http://localhost:3000** and allow camera access.

**Features Demo:**
1. Click camera icon to start detection
2. Position your face in front of the webcam
3. Close your eyes for 3+ seconds to trigger alarm
4. Toggle dark/light mode with moon/sun icon
5. Install as PWA via browser menu

---

## 🐍 Backend Setup (Optional)

The backend is currently not functional due to missing files. To restore:

### Option 1: Minimal Setup

Create a basic FastAPI server in `api/main.py`:

```python
from fastapi import FastAPI

app = FastAPI(title="SleepSafe API")

@app.get("/")
def read_root():
    return {"message": "SleepSafe Backend is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

Then run:
```bash
cd api
uv init  # Initialize project
uv add fastapi uvicorn
uv run uvicorn main:app --reload
```

### Option 2: Full Restoration

Restore from the original git commit (if available):

```bash
git log --all --full-history -- api/  # Find commits with api/ files
git checkout <commit-hash> -- api/    # Restore files
```

---

## 📱 Mobile Development

### Android

**Prerequisites:**
- Android Studio installed
- Android SDK 24+ (Android 7.0)
- Rust toolchain + cargo-ndk

**Steps:**

1. **Build Rust Core for Android:**
```bash
cd core
cargo install cargo-ndk
rustup target add aarch64-linux-android
cargo ndk -t arm64-v8a --platform 24 build --release
```

2. **Copy library to Android project:**
```bash
cp target/aarch64-linux-android/release/libsleep_core.so app/android/app/src/main/jniLibs/arm64-v8a/
```

3. **Open in Android Studio:**
```bash
# Open app/android/ folder in Android Studio
# Sync Gradle
# Build & Run
```

### iOS

**Prerequisites:**
- macOS with Xcode installed
- Rust toolchain + cargo-lipo

**Steps:**

1. **Build Rust Core for iOS:**
```bash
cd core
cargo install cargo-lipo
rustup target add aarch64-apple-ios x86_64-apple-ios
cargo lipo --release
```

2. **Open in Xcode:**
```bash
open app/ios/SleepDetection.xcodeproj
```

3. **Add library:**
- In Xcode, select project → Build Phases → Link Binary With Libraries
- Add `core/target/universal/release/libsleep_core.a`

4. **Configure Bridging Header:**
- Build Settings → Objective-C Bridging Header
- Set to `SleepDetection/SleepCoreBridge.h`

---

## 🐳 Docker Deployment

**Current Status:** Docker Compose file exists but references missing `api/` files.

**To Fix:**

1. Restore `api/` directory (see Backend Setup above)
2. Ensure `api/Dockerfile` exists
3. Run:
```bash
docker-compose up --build
```

**Services:**
- Web: http://localhost:80
- API: http://localhost:8000
- MLflow: http://localhost:5001

---

## ⚡ Performance Tuning

### Web App

Already optimized with:
- WebGL backend for TensorFlow.js
- Production mode enabled (`tf.enableProdMode()`)
- Aggressive Next.js optimizations

### Rust Core

Compiler optimizations in `core/Cargo.toml`:
```toml
[profile.release]
opt-level = 3        # Maximum optimization
lto = true           # Link-time optimization
codegen-units = 1    # Single codegen unit
panic = "abort"      # Smaller binary size
strip = true         # Remove debug symbols
```

---

## 🧪 Testing

### Web App Testing

```bash
cd web
npm run lint          # ESLint
npm run build         # Production build test
npm run start         # Production server
```

### Rust Core Testing

```bash
cd core
cargo test            # Run unit tests
cargo clippy          # Lint checks
```

---

## 📊 Monitoring

### Web App Metrics

- Check browser console for TensorFlow.js stats
- Network tab shows PWA caching
- Lighthouse audit for performance

### Backend Metrics (when restored)

- FastAPI `/docs` for API documentation
- MLflow UI for experiment tracking
- Health check endpoint: `/health`

---

## 🔧 Troubleshooting

### Web App Issues

**Problem:** TensorFlow.js fails to load
- **Solution:** Clear browser cache, reinstall node_modules

**Problem:** Camera not detected
- **Solution:** Check browser permissions, use HTTPS in production

**Problem:** TypeScript errors in IDE
- **Solution:** `npm install` to restore node_modules with proper types

### Rust Build Issues

**Problem:** JNI errors on Android
- **Solution:** Verify Android NDK is installed, check target arch

**Problem:** FFI linker errors on iOS
- **Solution:** Ensure library is added to Xcode project, rebuild

### Backend Issues

**Problem:** API returns 404
- **Solution:** `api/` directory is empty, see Backend Setup section

**Problem:** Docker build fails
- **Solution:** Ensure `api/Dockerfile` exists

---

## 📝 Next Steps

1. ✅ **Web App**: Fully functional - ready for production
2. 🔨 **Backend**: Restore `api/` files or recreate basic server
3. 🔨 **Mobile**: Compile Rust libraries and integrate
4. 🔨 **Libraries**: Publish to npm/PyPI (optional)
5. 🔨 **CI/CD**: Set up GitHub Actions for automated builds

---

## 🎯 Quick Demo Script

To showcase the project to others:

```bash
# Terminal 1: Start web app
cd web
npm run dev

# Terminal 2 (future): Start backend
cd api
uv run uvicorn main:app --reload

# Browser: Open http://localhost:3000
# Demo: Allow camera → Close eyes → Alarm sounds!
```

---

**Last Updated:** 2025-12-27  
**Project Status:** Web App ✅ | Backend ⏳ | Mobile 🏗️
