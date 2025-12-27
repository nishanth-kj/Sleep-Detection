# 🔬 MLOps in SleepSafe - Complete Guide

## 📊 What is MLOps?

**MLOps** (Machine Learning Operations) is the practice of versioning, tracking, and managing machine learning models in production. It combines:

- **ML**: Model training and evaluation
- **Ops**: Deployment, monitoring, and maintenance

In SleepSafe, MLOps enables us to:
- Track drowsiness detection experiments
- Version trained models
- Monitor model performance over time
- Compare different model configurations
- Reproduce results

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SleepSafe MLOps Flow                    │
└─────────────────────────────────────────────────────────────┘

1. DATA COLLECTION
   ┌──────────────┐
   │  Web/Mobile  │  Detects drowsiness
   │     App      │  (TensorFlow.js)
   └──────┬───────┘
          │
          ▼
   POST /telemetry
   {
     "ear_value": 0.18,
     "is_drowsy": true,
     "duration_ms": 4000
   }

2. DATA STORAGE
   ┌──────────────┐
   │   FastAPI    │  Receives telemetry
   │   Backend    │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  PostgreSQL  │  Stores events
   │   Database   │  (api/db/)
   └──────────────┘

3. MODEL TRAINING
   ┌──────────────┐
   │   Training   │  Reads historical data
   │   Pipeline   │  (api/mlops/train_model.py)
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │    MLflow    │  Tracks experiments
   │              │  Logs metrics & models
   └──────────────┘

4. MODEL DEPLOYMENT
   ┌──────────────┐
   │   MLflow     │  Serves best model
   │   Registry   │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  Production  │  Uses model for
   │     API      │  predictions
   └──────────────┘
```

---

## 🔄 Complete MLOps Workflow

### Step 1: Data Collection (Real-Time)

**Frontend (Web/Mobile)** detects drowsiness using TensorFlow.js:

```javascript
// web/app/page.tsx
const ear = calculateEAR(landmarks);
const isDrowsy = ear < EAR_THRESHOLD;

// Send to backend
fetch('http://localhost:8000/telemetry', {
  method: 'POST',
  body: JSON.stringify({
    ear_value: ear,
    is_drowsy: isDrowsy,
    duration_ms: 3500
  })
});
```

### Step 2: Backend Processing

**FastAPI** receives and processes events:

```python
# api/main.py
@app.post("/telemetry")
def log_detection_event(event: DetectionEvent):
    # Process event
    processed = detection_service.process_detection_event(
        ear_value=event.ear_value,
        is_drowsy=event.is_drowsy,
        duration_ms=event.duration_ms
    )
    
    # Log to MLflow
    run_id = mlflow_service.log_detection_event(...)
    
    # Save to database
    db_event = DetectionEventDB(**processed)
    session.add(db_event)
    session.commit()
    
    return {"status": "logged", "event_id": run_id}
```

### Step 3: MLflow Tracking

**MLflowService** tracks all experiments:

```python
# api/services/services.py
class MLflowService:
    def log_detection_event(self, ear_value, is_drowsy, duration_ms):
        with mlflow.start_run(experiment_id=self.experiment_id):
            # Log parameters
            mlflow.log_param("timestamp", timestamp)
            
            # Log metrics
            mlflow.log_metric("ear_value", ear_value)
            mlflow.log_metric("is_drowsy", 1 if is_drowsy else 0)
            mlflow.log_metric("duration_ms", duration_ms)
            
            return run.info.run_id
```

### Step 4: Model Training

**Training Pipeline** creates and evaluates models:

```python
# api/mlops/train_model.py
def train_model():
    # 1. Generate/Load Data
    X, y = generate_synthetic_data(n_samples=2000)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    
    # 2. Start MLflow Run
    with mlflow.start_run(run_name="random_forest_baseline"):
        # 3. Define Parameters
        params = {
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": 42
        }
        mlflow.log_params(params)
        
        # 4. Train Model
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        
        # 5. Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # 6. Log Metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        
        # 7. Save Model
        mlflow.sklearn.log_model(
            model, 
            "model",
            registered_model_name="drowsiness_detector"
        )
```

### Step 5: Model Versioning

**MLflow Registry** manages model versions:

```
Models:
  └── drowsiness_detector
      ├── Version 1: accuracy=0.92 (staging)
      ├── Version 2: accuracy=0.95 (production) ← Best
      └── Version 3: accuracy=0.93 (archived)
```

### Step 6: Model Deployment

**Load and use the best model**:

```python
# Future: Load production model
import mlflow.sklearn

model_uri = "models:/drowsiness_detector/production"
model = mlflow.sklearn.load_model(model_uri)

# Make predictions
prediction = model.predict([[ear, variance, duration, time]])
```

---

## 📁 File Structure

```
api/
├── mlops/
│   ├── __init__.py
│   └── train_model.py          # Training pipeline
│
├── services/
│   └── services.py
│       ├── MLflowService       # Experiment tracking
│       ├── DetectionService    # Data processing
│       └── AnalyticsService    # Insights
│
├── db/
│   ├── models.py               # Database models
│   ├── sleepsafe.db            # SQLite (dev)
│   └── postgres/               # PostgreSQL (prod)
│
└── mlruns/                     # MLflow experiments
    └── 0/                      # Experiment ID
        ├── run1/               # First training run
        ├── run2/               # Second training run
        └── ...
```

---

## 🚀 Running MLOps

### 1. Start Backend (Tracking Server)

```bash
cd api
uv run uvicorn main:app --reload
```

Backend runs on: http://localhost:8000

### 2. Log Detection Events

```bash
# Log event manually
curl -X POST http://localhost:8000/telemetry \
  -H "Content-Type: application/json" \
  -d '{
    "ear_value": 0.18,
    "is_drowsy": true,
    "duration_ms": 4000
  }'
```

### 3. Train Model

```bash
cd api
uv run python mlops/train_model.py
```

Output:
```
Starting model training...
Generating synthetic training data...
Training Random Forest model...
Model Metrics:
  Accuracy:  0.9500
  Precision: 0.9200
  Recall:    0.9400
  F1-Score:  0.9300
✅ Model training completed successfully!
```

### 4. View Experiments (MLflow UI)

```bash
# Option 1: Docker
docker compose up mlflow_ui -d

# Option 2: Local
cd api
uv run mlflow ui --backend-store-uri postgresql://... --port 5000
```

Access: http://localhost:5001

### 5. Compare Runs

In MLflow UI:
1. Click "Experiments"
2. Select "drowsiness_detection"
3. Compare metrics across runs
4. Select best model

---

## 📊 MLflow UI Features

### Experiments View

```
┌─────────────────────────────────────────────────┐
│  Experiment: drowsiness_detection               │
├─────────────────────────────────────────────────┤
│  Run Name          │ Accuracy │ Precision │ F1  │
├────────────────────┼──────────┼───────────┼─────┤
│  random_forest_v1  │  0.92    │  0.89     │ 0.90│
│  random_forest_v2  │  0.95    │  0.92     │ 0.93│ ← Best
│  decision_tree_v1  │  0.88    │  0.85     │ 0.86│
└────────────────────┴──────────┴───────────┴─────┘
```

### Run Details

```
Run: random_forest_v2
├── Parameters
│   ├── n_estimators: 100
│   ├── max_depth: 10
│   └── random_state: 42
│
├── Metrics
│   ├── accuracy: 0.95
│   ├── precision: 0.92
│   ├── recall: 0.94
│   └── f1_score: 0.93
│
└── Artifacts
    ├── model/           # Saved model
    └── confusion_matrix.png
```

---

## 🔬 Experiment Tracking

### What Gets Tracked?

1. **Parameters** (Model Config)
   ```python
   mlflow.log_param("n_estimators", 100)
   mlflow.log_param("max_depth", 10)
   ```

2. **Metrics** (Performance)
   ```python
   mlflow.log_metric("accuracy", 0.95)
   mlflow.log_metric("f1_score", 0.93)
   ```

3. **Models** (Trained Artifacts)
   ```python
   mlflow.sklearn.log_model(model, "model")
   ```

4. **Metadata** (Timestamps, User, etc.)
   - Start time
   - End time
   - Status (RUNNING, FINISHED, FAILED)

---

## 📈 Real-World Workflow

### Daily Operations

```bash
# Morning: Check data quality
curl http://localhost:8000/statistics

# Collect data throughout the day
# (Automatic via web/mobile apps)

# Evening: Train model with new data
docker compose run --rm ml_training

# Review results in MLflow UI
open http://localhost:5001

# Deploy best model
# (Manual promotion to production)
```

### Monthly Improvements

1. **Analyze Performance**
   - Check MLflow for model drift
   - Review detection accuracy

2. **Retrain Models**
   - Use accumulated data
   - Try new algorithms
   - Tune hyperparameters

3. **A/B Testing**
   - Deploy new model to 10% users
   - Compare with current model
   - Rollout if better

---

## 🗄️ Data Flow

```
User Detection → Web App → Backend API → Database
                              ↓
                         MLflow Tracking
                              ↓
                    Experiment Logged
                              ↓
Training Pipeline ← Database ← Query Data
        ↓
   Train Model
        ↓
    Evaluate
        ↓
Log to MLflow
        ↓
   Save Model
        ↓
Model Registry → Production Deployment
```

---

## 🔄 Docker MLOps

### Services

```yaml
# docker-compose.yml
services:
  postgres:       # Data storage
  backend:        # API + Tracking server
  mlflow_ui:      # Experiment visualization
  ml_training:    # Model training (on-demand)
```

### Run Training in Docker

```bash
# One-time training
docker compose run --rm ml_training

# Or with profile
docker compose --profile training up ml_training
```

---

## 📊 Monitoring & Analytics

### Get Statistics

```bash
curl http://localhost:8000/statistics
```

Response:
```json
{
  "total_events": 1234,
  "drowsy_events": 456,
  "average_ear": 0.28,
  "average_duration_ms": 2500,
  "drowsiness_rate": 36.95
}
```

### Dashboard

```bash
curl http://localhost:8000/dashboard
```

Response:
```json
{
  "overall": { 
    "total_events": 1234,
    "drowsy_events": 456
  },
  "last_hour": {
    "events_count": 45,
    "drowsy_count": 12,
    "alert_rate": 26.67
  },
  "status": "normal",
  "timestamp": "2025-12-27T13:30:00Z"
}
```

---

## ✅ Benefits of This MLOps Setup

### 1. **Reproducibility**
Every experiment is tracked - can reproduce any result

### 2. **Comparison**
Easy to compare different models and parameters

### 3. **Versioning**
All models are versioned and can be rolled back

### 4. **Monitoring**
Track model performance over time

### 5. **Collaboration**
Team members can see all experiments

### 6. **Automation**
Training pipeline can be automated

---

## 🎯 Summary

**SleepSafe MLOps enables:**

1. ✅ **Data Collection** - Frontend logs detection events
2. ✅ **Storage** - PostgreSQL stores all data
3. ✅ **Tracking** - MLflow tracks experiments
4. ✅ **Training** - Automated model training
5. ✅ **Evaluation** - Compare model metrics
6. ✅ **Versioning** - Model registry
7. ✅ **Deployment** - Best model to production
8. ✅ **Monitoring** - Performance analytics

**Access Points:**
- API: http://localhost:8000
- MLflow: http://localhost:5001
- Database: PostgreSQL (port 5432)

---

**Now you have a complete MLOps pipeline for drowsiness detection!** 🎊
