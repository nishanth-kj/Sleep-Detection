# 📚 Documentation Index

Complete documentation for SleepSafe drowsiness detection system.

## 🚀 Quick Links

| Document | Description |
|----------|-------------|
| [README.md](../README.md) | Main project overview |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design & architecture |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deployment guide |
| [DATABASE-STRUCTURE.md](DATABASE-STRUCTURE.md) | Django-style database setup |
| [BACKEND-COMPLETE.md](BACKEND-COMPLETE.md) | Backend API features |
| [DOCKER.md](DOCKER.md) | Docker setup guide |

## 📁 Project Structure

```
Sleep-Detection/
├── web/              # Next.js PWA (✅ Complete)
├── api/              # FastAPI Backend (✅ Complete)
│   └── db/           # Django-style database
├── core/             # Rust library (✅ Code complete)
├── app/              # iOS/Android apps (🏗️ In progress)
└── docs/             # This directory
```

## ✅ Current Status

### Complete & Running
- ✅ Web PWA at http://localhost:3000
- ✅ Backend API at http://localhost:8000
- ✅ API Docs at http://localhost:8000/docs
- ✅ Docker setup (multi-container)
- ✅ Database (SQLite + PostgreSQL)
- ✅ MLOps with MLflow

### In Progress
- 🏗️ Mobile app integration
- 🏗️ Rust library compilation
- 🏗️ NPM/PyPI package publication

## 📖 Documentation Guide

### For Developers

1. **Start Here**: [README.md](../README.md)
2. **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Database**: [DATABASE-STRUCTURE.md](DATABASE-STRUCTURE.md)
4. **Backend**: [BACKEND-COMPLETE.md](BACKEND-COMPLETE.md)

### For DevOps

1. **Docker**: [DOCKER.md](DOCKER.md)
2. **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)

### For Mobile Developers

1. **Main README**: Mobile setup section
2. **Architecture**: Core integration details

## 🔧 Quick Commands

### Web
```bash
cd web && npm run dev
```

### Backend
```bash
cd api && uv run uvicorn main:app --reload
```

### Docker
```bash
docker compose up -d
```

### Database
```bash
cd api && uv run python -c "from db import init_db; init_db()"
```

## 📊 Database Location

**Django-style**: All database files in `api/db/`

- SQLite: `api/db/sleepsafe.db`
- PostgreSQL: `api/db/postgres/`
- Backups: `api/db/backups/`

## 🆘 Getting Help

1. Check relevant documentation above
2. View API docs: http://localhost:8000/docs
3. Check logs: `docker compose logs -f`

---

**Last Updated**: 2025-12-27  
**Status**: ✅ All documentation current
