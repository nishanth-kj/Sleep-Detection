# 😴 SleepSafe - AI-Powered Drowsiness Detection System

<div align="center">

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Web%20%7C%20iOS%20%7C%20Android-lightgrey.svg)

**Real-time drowsiness detection using computer vision and machine learning**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation)

</div>

---

## 🎯 Overview

SleepSafe is a **cross-platform drowsiness detection ecosystem** that prevents accidents caused by fatigue. Using advanced **computer vision** and **AI**, the system monitors eye closure patterns in real-time and triggers alerts when drowsiness is detected.

### 🌟 Key Highlights

- 🌐 **Offline-First Web App**: Progressive Web App with TensorFlow.js for browser-based detection
- 📱 **Native Mobile Apps**: iOS (Swift) and Android (Java) with shared Rust core
- 🦀 **High-Performance Rust Core**: Memory-safe, optimized logic shared across platforms
- 🎨 **Beautiful UI**: Glassmorphism design with dark/light modes
- 🔒 **Privacy-Focused**: All processing happens on-device, no data leaves your machine
- ⚡ **Real-Time Performance**: Optimized for low-latency detection (< 100ms)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         SleepSafe Ecosystem                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Web PWA    │  │  Android App │  │     iOS App          │  │
│  │  (Next.js)   │  │   (Java)     │  │     (Swift)          │  │
│  │  TensorFlow  │  │     JNI      │  │       FFI            │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                       │              │
│         │                 └───────────┬───────────┘              │
│         │                             │                          │
│         │                      ┌──────▼──────────┐               │
│         │                      │   Rust Core     │               │
│         │                      │  (libsleep)     │               │
│         │                      └─────────────────┘               │
│         │                                                        │
│    ┌────▼──────────────────────────────────────────┐            │
│    │         MediaPipe Face Mesh                    │            │
│    │    (468 Facial Landmarks Detection)            │            │
│    └────────────────────────────────────────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
Sleep-Detection/
│
├── 🌐 web/                    # Next.js Progressive Web App
│   ├── app/
│   │   ├── page.tsx           # Main detection interface
│   │   ├── layout.tsx         # App shell
│   │   └── globals.css        # Global styles
│   ├── public/
│   │   ├── manifest.json      # PWA manifest
│   │   └── icons/             # App icons
│   ├── package.json           # Dependencies
│   └── Dockerfile             # Container config
│
├── 🐍 api/                    # FastAPI Backend
│   ├── main.py                # API entry point
│   ├── models/                # Pydantic models
│   │   ├── __init__.py
│   │   └── models.py
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   └── services.py
│   ├── mlops/                 # ML training
│   │   ├── __init__.py
│   │   └── train_model.py
│   ├── db/                    # Database (Django-style)
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── sleepsafe.db       # SQLite database
│   │   └── postgres/          # PostgreSQL data (Docker)
│   ├── pyproject.toml
│   └── Dockerfile
│
├── 🦀 core/                   # Rust Shared Library
│   ├── src/
│   │   └── lib.rs             # FFI/JNI exports
│   └── Cargo.toml             # Rust dependencies
│
├── 📱 app/                    # Native Mobile Apps
│   ├── android/               # Android Application
│   │   └── app/src/main/
│   │       ├── java/.../MainActivity.java
│   │       └── AndroidManifest.xml
│   │
│   └── ios/                   # iOS Application
│       └── SleepDetection/
│           ├── ViewController.swift
│           ├── AppDelegate.swift
│           └── SleepCoreBridge.h  # C bridge for Rust
│
├── 📦 lib/                    # Future Libraries
│   ├── npm/                   # (Planned) NPM package
│   └── pypi/                  # (Planned) PyPI package
│
├── 📚 docs/                   # Documentation
│   ├── ARCHITECTURE.md        # System design
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── DATABASE-STRUCTURE.md  # Database setup
│   ├── BACKEND-COMPLETE.md    # Backend features
│   └── DOCKER.md              # Docker guide
│
├── docker-compose.yml         # Multi-container orchestration
├── .env.example               # Environment template
└── README.md                  # This file
```

---

## 🚀 Quick Start

### Prerequisites

| Component | Requirement |
|-----------|-------------|
| **Web** | Node.js 18+, npm 8+ |
| **Mobile** | Android Studio / Xcode |
| **Rust** | Rust 1.70+ (for core compilation) |

### 2️⃣ Backend API (Python + FastAPI)

The backend provides telemetry logging and MLOps features:

```bash
cd api

# Install dependencies
uv sync

# Run development server
uv run uvicorn main:app --reload
```

🔧 **API Docs**: http://localhost:8000/docs

**Features:**
- Detection event logging
- Model metrics tracking
- MLflow experiment tracking
- Statistics and analytics
- Database: `api/db/sleepsafe.db` (Django-style)

**Endpoints:**
- `POST /telemetry` - Log detection event
- `GET /statistics` - Get stats
- `GET /dashboard` - Dashboard data  
- `POST /metrics/model` - Log model metrics

**Note:** Backend is fully functional with SQLite. PostgreSQL optional for production.

### 🌐 Web Application (Recommended)

The web app is **fully functional** and works offline:

```bash
# Clone repository
git clone https://github.com/nishanth-kj/Sleep-Detection.git
cd Sleep-Detection/web

# Install dependencies
npm install

# Start development server
npm run dev
```

📱 Open **http://localhost:3000** in your browser

#### **How to Use:**
1. Click the **camera icon** to start detection
2. Allow camera access when prompted
3. Position your face in the webcam view
4. Close your eyes for 3+ seconds to trigger the alarm
5. Toggle **dark/light mode** with the moon/sun icon

---

### 📱 Mobile Apps

#### **Android Development**

##### Step 1: Build Rust Core

```bash
cd core
rustup target add aarch64-linux-android
cargo install cargo-ndk
cargo ndk -t arm64-v8a --platform 24 build --release
```

##### Step 2: Copy Library

```bash
mkdir -p app/android/app/src/main/jniLibs/arm64-v8a
cp target/aarch64-linux-android/release/libsleep_core.so \
   app/android/app/src/main/jniLibs/arm64-v8a/
```

##### Step 3: Open in Android Studio

```bash
# Open app/android/ folder
android-studio app/android
```

Build and run on device or emulator.

---

#### **iOS Development**

##### Step 1: Build Rust Core

```bash
cd core
rustup target add aarch64-apple-ios x86_64-apple-ios
cargo install cargo-lipo
cargo lipo --release
```

##### Step 2: Configure Xcode

1. Open `app/ios/SleepDetection.xcodeproj` in Xcode
2. Add `core/target/universal/release/libsleep_core.a` to **Link Binary With Libraries**
3. Set **Objective-C Bridging Header** to `SleepDetection/SleepCoreBridge.h`
4. Build and run on device/simulator

---

## 🧠 How It Works

### Detection Algorithm: Eye Aspect Ratio (EAR)

The system uses the **Eye Aspect Ratio** metric to detect eye closure:

```
       ||p2 - p6|| + ||p3 - p5||
EAR = ───────────────────────────
           2 × ||p1 - p4||

Where p1...p6 are eye landmark coordinates
```

**Detection Logic:**
- EAR > 0.25 → Eyes **OPEN** ✅
- EAR < 0.25 for **10 consecutive frames** (≈ 3 seconds) → **DROWSINESS DETECTED** 🚨

### Technology Stack

#### Web Frontend
- **Framework**: Next.js 16.1 (React 19.2)
- **AI/ML**: TensorFlow.js 4.22, MediaPipe Face Mesh 1.0
- **Styling**: TailwindCSS 3.4, Framer Motion 12.23
- **PWA**: next-pwa 5.6 for offline support
- **Utilities**: react-webcam, lucide-react icons

#### Mobile Core
- **Language**: Rust 2021 Edition
- **Build**: Cargo with aggressive optimizations
- **Features**:
  - `opt-level = 3` - Maximum optimization
  - `lto = true` - Link-time optimization
  - `codegen-units = 1` - Single compilation unit
  - `panic = "abort"` - Smaller binary size

#### Native Integrations
- **Android**: JNI (Java Native Interface)
- **iOS**: FFI (Foreign Function Interface) via C bridge

---

## ✨ Features

### Core Functionality

✅ **Real-Time Face Detection**
- 468 facial landmarks tracked at 30 FPS
- MediaPipe Face Mesh model (optimized for web)

✅ **Eye Closure Monitoring**
- Continuous EAR calculation for both eyes
- Configurable threshold and frame count

✅ **Smart Alerting**
- Audio alarm using Web Audio API
- Visual on-screen alerts
- Mute/unmute toggle

✅ **Offline Capability**
- PWA with service worker caching
- Install to home screen (mobile/desktop)
- Works without internet after first load

✅ **Dark/Light Modes**
- System preference detection
- Manual toggle
- Smooth transitions

### UI/UX

🎨 **Modern Design**
- Glassmorphism effects
- Smooth animations with Framer Motion
- Responsive layout (mobile-first)

📊 **Live Statistics**
- Current EAR value display
- Online/offline indicator
- FPS counter
- Detection status

---

## 🐳 Docker Deployment

**Note:** Docker Compose currently references an empty `api/` directory. To run only the web app:
Run the complete stack with Docker:

```bash
docker compose up -d --build
```

**Services:**
- **Frontend**: http://localhost:80 (Next.js PWA)
- **Backend API**: http://localhost:8000 (FastAPI)
- **MLflow UI**: http://localhost:5001 (Experiment tracking)
- **PostgreSQL**: Port 5432 (Database)

**Data Persistence:**
- PostgreSQL: `api/db/postgres/`
- MLruns: `api/mlruns/`

**Commands:**
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all
docker compose down

# Run ML training
docker compose --profile training up ml_training
```

---

## 📚 Documentation

- 📖 **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design, diagrams, data flow
- 🚀 **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Detailed deployment instructions
- 💻 **Code Comments** - Inline documentation in all source files

---

## 🔒 Privacy & Security

### On-Device Processing
- **NO** data is sent to external servers
- Facial landmarks processed locally
- Web app works 100% offline

### Data Storage
- **NO** persistent storage of video/images
- **NO** tracking or analytics
- Optional browser cache for PWA only

### Permissions
- **Camera**: Required for face detection
- **Audio**: For alarm playback (Web Audio API)

---

## 🛠️ Development

### Web App Commands

```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm run start    # Run production server
npm run lint     # Run ESLint
```

### Rust Core Commands

```bash
cargo build --release  # Build optimized library
cargo test             # Run unit tests
cargo clippy           # Lint checks
cargo fmt              # Format code
```

### Environment Variables

None required! The app works out-of-the-box.

---

## 🐛 Known Issues & Roadmap

### Current Status

| Component | Status |
|-----------|--------|
| Web PWA | ✅ Fully Functional |
| Rust Core | ✅ Code Complete |
| Android App | 🏗️ Skeleton Code |
## 🐛 Current Status & TODOs

### ✅ Complete & Working
- [x] Web PWA (Next.js + TensorFlow.js)
- [x] Backend API (FastAPI + SQLAlchemy)
- [x] Database (SQLite + PostgreSQL support)
- [x] MLOps (MLflow + training pipeline)
- [x] Docker setup (multi-container)
- [x] Documentation (comprehensive)

### 🏗️ In Progress
- [ ] Compile Rust core for Android (`libsleep_core.so`)
- [ ] Compile Rust core for iOS (`libsleep_core.a`)  
- [ ] Integrate Rust with mobile apps
- [ ] Publish NPM package (`lib/npm`)
- [ ] Publish PyPI package (`lib/pypi`)

### 📊 Database
- **Location**: `api/db/` (Django-style)
- **SQLite**: `api/db/sleepsafe.db`
- **PostgreSQL**: `api/db/postgres/` (Docker)
- **Models**: 4 tables (events, metrics, sessions, system) support
- [ ] Customizable EAR thresholds
- [ ] Bluetooth alerting (mobile)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Setup all components
npm install       # Web dependencies
cargo build       # Rust core
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **MediaPipe** team for Face Mesh model
- **TensorFlow.js** for browser ML capabilities
- **Rust** community for FFI/JNI tooling
- **Next.js** team for the amazing framework

---

## 📧 Contact & Support

- **Author**: Nishanth KJ
- **GitHub**: [@nishanth-kj](https://github.com/nishanth-kj)
- **Repository**: [Sleep-Detection](https://github.com/nishanth-kj/Sleep-Detection)
- **Issues**: [Report a Bug](https://github.com/nishanth-kj/Sleep-Detection/issues)

---

<div align="center">

**Made with ❤️ for safer roads and workplaces**

⭐ Star this repo if you find it useful!

</div>