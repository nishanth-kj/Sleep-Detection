# ✅ Django-Style Database Structure - Complete!

## 📁 New Structure (Like Django)

All database files are now in `api/db/`:

```
api/
└── db/
    ├── __init__.py           # Package exports
    ├── database.py           # SQLAlchemy config
    ├── models.py             # Database models
    ├── .gitignore            # Exclude DB files
    ├── sleepsafe.db          # SQLite database
    ├── postgres/             # PostgreSQL data (Docker)
    └── backups/              # Database backups
```

## 🔧 Configuration

### Database Path

**Local Development:**
```python
# api/db/database.py
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(DB_DIR, 'sleepsafe.db')}"
```

Database file: `api/db/sleepsafe.db`

### Environment Variables

```bash
# .env
DATABASE_URL=sqlite:///api/db/sleepsafe.db
MLFLOW_TRACKING_URI=sqlite:///api/db/sleepsafe.db
```

## 🐳 Docker Volumes

All volumes now point to `api/db`:

```yaml
volumes:
  - ./api/mlruns:/app/mlruns
  - ./api/db:/app/db

postgres:
  volumes:
    - ./api/db/postgres:/var/lib/postgresql/data
```

## 🚀 Usage

### Initialize Database

```bash
cd api
uv run python -c "from db import init_db; init_db()"
```

### Start Backend

```bash
cd api
uv run uvicorn main:app --reload
```

Database will be created at `api/db/sleepsafe.db`

### Docker

```bash
docker compose up -d
```

PostgreSQL data: `api/db/postgres/`

## 🗃️ Database Models

1. **DetectionEventDB** - `api/db/models.py`
2. **ModelMetricsDB** - `api/db/models.py`
3. **SystemEventDB** - `api/db/models.py`
4. **UserSessionDB** - `api/db/models.py`

## 📝 Import Examples

```python
from db import init_db, SessionLocal, DetectionEventDB

# Initialize
init_db()

# Use session
session = SessionLocal()
events = session.query(DetectionEventDB).all()
```

## ✅ Changes Made

- ✅ Removed root `db/` folder
- ✅ All database code in `api/db/`
- ✅ SQLite file: `api/db/sleepsafe.db`
- ✅ PostgreSQL data: `api/db/postgres/`
- ✅ Updated docker-compose.yml volumes
- ✅ Updated .env.example paths
- ✅ Added api/db/.gitignore

---

**Status**: ✅ Django-style structure complete  
**Location**: `api/db/`  
**Database**: `api/db/sleepsafe.db`
