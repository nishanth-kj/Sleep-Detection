# 🔬 MLOps Quick Start

## What is MLOps in SleepSafe?

MLOps = **Machine Learning Operations**

It's how we:
- ✅ Track experiments
- ✅ Version models  
- ✅ Monitor performance
- ✅ Reproduce results

## How It Works (Simple)

```
1. USER DETECTS DROWSINESS
   👤 Web App → EAR = 0.18 → Drowsy!
   
2. DATA LOGGED
   📊 POST /telemetry → Backend API → Database
   
3. MODEL TRAINS
   🎓 Python reads data → Trains classifier → Saves model
   
4. MLFLOW TRACKS
   📈 Logs: accuracy=0.95, precision=0.92
   
5. BEST MODEL DEPLOYED
   🚀 Version 2 (best) → Production
```

## Quick Commands

### Log Detection Event
```bash
curl -X POST http://localhost:8000/telemetry \
  -H "Content-Type: application/json" \
  -d '{"ear_value": 0.18, "is_drowsy": true, "duration_ms": 4000}'
```

### Train Model
```bash
# Docker
docker compose run --rm ml_training

# Local
cd api && uv run python mlops/train_model.py
```

### View Experiments
```bash
# Open MLflow UI
open http://localhost:5001
```

### Check Statistics
```bash
curl http://localhost:8000/statistics
```

## What Gets Tracked?

### Parameters (Config)
- n_estimators: 100
- max_depth: 10
- algorithm: random_forest

### Metrics (Performance)
- accuracy: 0.95
- precision: 0.92
- recall: 0.94
- f1_score: 0.93

### Models (Files)
- Trained model saved
- Can reload anytime
- Version controlled

## Visual Flow

```
┌─────────────┐
│   Web App   │  Detects drowsiness
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Backend API │  Logs event
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Database   │  Stores data
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Training   │  Trains model
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   MLflow    │  Tracks experiment
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Production  │  Best model deployed
└─────────────┘
```

## Benefits

1. **Never Lose Results** - All experiments saved
2. **Easy Comparison** - See which model is best
3. **Rollback** - Can go back to previous version
4. **Team Collaboration** - Everyone sees same data
5. **Automated** - Training can run automatically

## Access Points

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs  
- **MLflow UI**: http://localhost:5001
- **Database**: PostgreSQL (port 5432)

## Full Guide

📖 See [MLOPS-GUIDE.md](MLOPS-GUIDE.md) for complete documentation

---

**Status**: ✅ MLOps fully operational!
