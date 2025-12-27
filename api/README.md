# 🐍 SleepSafe Backend API

FastAPI backend for drowsiness detection telemetry and MLOps.

## 🏗️ Architecture

```
api/
├── main.py              # FastAPI application entry point
├── models/              # Pydantic models for validation
│   ├── __init__.py
│   └── models.py        # Request/response models
├── services/            # Business logic layer
│   ├── __init__.py
│   └── services.py      # MLflow, Detection, Analytics services
├── mlops/               # Machine learning operations
│   ├── __init__.py
│   └── train_model.py   # Model training script
├── pyproject.toml       # UV dependencies
├── Dockerfile           # Container configuration
└── .gitignore           # Git exclusions
```

## 🚀 Quick Start

### Using UV (Recommended)

```bash
cd api

# Install dependencies
uv sync

# Run development server
uv run uvicorn main:app --reload

# Run ML training
uv run python mlops/train_model.py
```

### API Access

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### Health & Status

- `GET /` - API root information
- `GET /health` - Health check with uptime

### Telemetry

- `POST /telemetry` - Log single detection event
- `POST /telemetry/batch` - Log multiple events

**Example Request:**
```json
{
  "ear_value": 0.15,
  "is_drowsy": true,
  "duration_ms": 3500
}
```

### Analytics

- `GET /statistics` - Overall detection statistics
- `GET /dashboard` - Comprehensive dashboard data
- `GET /events/recent?limit=50` - Recent events

### MLOps

- `POST /metrics/model` - Log model performance metrics
- `GET /mlflow/runs?max_results=10` - Get MLflow runs

### Admin

- `DELETE /events/cache` - Clear event cache

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Log detection event
curl -X POST http://localhost:8000/telemetry \
  -H "Content-Type: application/json" \
  -d '{"ear_value": 0.2, "is_drowsy": true, "duration_ms": 2000}'

# Get statistics
curl http://localhost:8000/statistics
```

## 🐳 Docker

### Build & Run

```bash
# From project root
docker compose up backend -d

# View logs
docker compose logs -f backend

# Run ML training
docker compose run --rm ml_training
```

## 📊 MLflow Integration

The backend integrates MLflow for experiment tracking:

- **Tracking URI**: `sqlite:///mlflow.db`
- **Experiment**: `drowsiness_detection`
- **Metrics**: EAR values, drowsiness events, model performance

### View MLflow UI

```bash
# Start MLflow UI
docker compose up mlflow_ui

# Access at http://localhost:5001
```

## 🔧 Configuration

### Environment Variables

- `MLFLOW_TRACKING_URI` - MLflow tracking database (default: `sqlite:///mlflow.db`)

### Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **mlflow** - Experiment tracking
- **pydantic** - Data validation
- **scikit-learn** - ML training
- **numpy** - Numerical computing

## 📝 Development

### Project Structure

- `models/` - Data validation schemas
- `services/` - Business logic (MLflow, Detection, Analytics)
- `mlops/` - ML training scripts

### Adding New Endpoints

1. Define Pydantic models in `models/models.py`
2. Add business logic to appropriate service in `services/`
3. Create endpoint in `main.py`
4. Update this README

## 🧩 Service Layer

### MLflowService
- Log detection events
- Log model metrics
- Query experiment runs

### DetectionService
- Process detection events
- Calculate severity
- Maintain event cache
- Provide statistics

### AnalyticsService
- Hourly summaries
- Dashboard data
- System status

## 🚨 Error Handling

All endpoints return standardized error responses:

```json
{
  "detail": "Error message",
  "status_code": 500,
  "timestamp": "2025-12-27T12:00:00.000Z"
}
```

## 📦 Deployment

### Production Setup

1. **Environment**: Set `MLFLOW_TRACKING_URI` to production database
2. **CORS**: Configure allowed origins in `main.py`
3. **Database**: Use PostgreSQL for MLflow instead of SQLite
4. **Monitoring**: Add application monitoring (Sentry, Prometheus)

### Docker Compose

```bash
# Start all services
docker compose up -d

# Frontend: http://localhost:80
# Backend: http://localhost:8000
# MLflow: http://localhost:5001
```

## 🔬 Machine Learning

### Training Pipeline

The `mlops/train_model.py` script:
1. Generates synthetic drowsiness data
2. Trains Random Forest classifier
3. Logs metrics to MLflow
4. Registers model

**Run Training:**
```bash
uv run python mlops/train_model.py
```

## 📈 Monitoring

- **Logs**: Check `/api/logs` or `docker compose logs backend`
- **Health**: Monitor `/health` endpoint
- **MLflow**: Track experiments at http://localhost:5001

## 🤝 Contributing

1. Add features to appropriate service
2. Update Pydantic models
3. Add tests (future)
4. Update documentation

---

**Status**: ✅ Backend Running  
**Port**: 8000  
**Docs**: http://localhost:8000/docs
