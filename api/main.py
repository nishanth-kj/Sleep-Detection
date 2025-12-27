"""
SleepSafe Backend API - FastAPI application for drowsiness detection telemetry
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime
import time

from models import (
    DetectionEvent,
    DetectionResponse,
    ModelMetrics,
    BatchDetectionRequest,
    StatisticsResponse,
    HealthResponse,
    DashboardSummary,
    ErrorResponse
)
from services import MLflowService, DetectionService, AnalyticsService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global services
mlflow_service: MLflowService = None
detection_service: DetectionService = None
analytics_service: AnalyticsService = None
app_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    global mlflow_service, detection_service, analytics_service
    
    logger.info("Initializing services...")
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
    
    mlflow_service = MLflowService(tracking_uri=mlflow_uri)
    detection_service = DetectionService()
    analytics_service = AnalyticsService(detection_service)
    
    logger.info("Services initialized successfully")
    yield
    
    logger.info("Shutting down services...")


# Create FastAPI app
app = FastAPI(
    title="SleepSafe Backend API",
    description="MLOps backend for drowsiness detection telemetry and analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            detail=str(exc),
            status_code=500,
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


# === Root Endpoints ===

@app.get("/", tags=["Root"])
def read_root():
    """API root endpoint with service information"""
    return {
        "service": "SleepSafe Backend API",
        "version": "1.0.0",
        "status": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "health": "/health",
            "telemetry": "/telemetry",
            "statistics": "/statistics",
            "dashboard": "/dashboard",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Health check endpoint"""
    uptime = time.time() - app_start_time
    return HealthResponse(
        status="healthy",
        mlflow_uri=mlflow_service.tracking_uri,
        timestamp=datetime.utcnow().isoformat(),
        uptime_seconds=round(uptime, 2)
    )


# === Telemetry Endpoints ===

@app.post("/telemetry", response_model=DetectionResponse, tags=["Telemetry"])
def log_detection_event(event: DetectionEvent):
    """
    Log a single drowsiness detection event
    
    - **ear_value**: Eye Aspect Ratio (0.0 - 1.0)
    - **is_drowsy**: Boolean indicating if drowsiness was detected
    - **duration_ms**: Duration of the state in milliseconds
    """
    try:
        # Process event through service
        processed_event = detection_service.process_detection_event(
            ear_value=event.ear_value,
            is_drowsy=event.is_drowsy,
            duration_ms=event.duration_ms,
            timestamp=event.timestamp
        )
        
        # Log to MLflow
        run_id = mlflow_service.log_detection_event(
            ear_value=event.ear_value,
            is_drowsy=event.is_drowsy,
            duration_ms=event.duration_ms,
            timestamp=processed_event["timestamp"]
        )
        
        return DetectionResponse(
            status="logged",
            event_id=run_id,
            timestamp=processed_event["timestamp"],
            severity=processed_event["severity"]
        )
    
    except Exception as e:
        logger.error(f"Failed to log detection event: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log event: {str(e)}"
        )


@app.post("/telemetry/batch", tags=["Telemetry"])
def log_batch_events(batch: BatchDetectionRequest):
    """Log multiple detection events in a single request"""
    try:
        results = []
        for event in batch.events:
            processed = detection_service.process_detection_event(
                ear_value=event.ear_value,
                is_drowsy=event.is_drowsy,
                duration_ms=event.duration_ms,
                timestamp=event.timestamp
            )
            results.append(processed)
        
        return {
            "status": "success",
            "events_logged": len(results),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Failed to log batch events: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log batch: {str(e)}"
        )


# === Statistics Endpoints ===

@app.get("/statistics", response_model=StatisticsResponse, tags=["Analytics"])
def get_statistics():
    """
    Get aggregated detection statistics
    
    Returns overall statistics from all cached detection events
    """
    try:
        stats = detection_service.get_statistics()
        return StatisticsResponse(**stats)
    
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )


@app.get("/dashboard", response_model=DashboardSummary, tags=["Analytics"])
def get_dashboard():
    """
    Get comprehensive dashboard data
    
    Returns overall statistics, hourly summary, and system status
    """
    try:
        summary = analytics_service.get_dashboard_summary()
        return DashboardSummary(**summary)
    
    except Exception as e:
        logger.error(f"Failed to get dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve dashboard: {str(e)}"
        )


@app.get("/events/recent", tags=["Analytics"])
def get_recent_events(limit: int = 50):
    """Get recent detection events"""
    try:
        events = detection_service.get_recent_events(limit=limit)
        return {
            "events": events,
            "count": len(events),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Failed to get recent events: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve events: {str(e)}"
        )


# === MLOps Endpoints ===

@app.post("/metrics/model", tags=["MLOps"])
def log_model_metrics(metrics: ModelMetrics):
    """
    Log model performance metrics
    
    - **accuracy**: Model accuracy (0.0 - 1.0)
    - **precision**: Model precision (0.0 - 1.0)
    - **recall**: Model recall (0.0 - 1.0)
    - **f1_score**: F1 score (optional)
    """
    try:
        run_id = mlflow_service.log_model_metrics(
            accuracy=metrics.accuracy,
            precision=metrics.precision,
            recall=metrics.recall,
            f1_score=metrics.f1_score
        )
        
        return {
            "status": "logged",
            "run_id": run_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Failed to log model metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log metrics: {str(e)}"
        )


@app.get("/mlflow/runs", tags=["MLOps"])
def get_mlflow_runs(max_results: int = 10):
    """Get recent MLflow runs"""
    try:
        runs = mlflow_service.get_recent_runs(max_results=max_results)
        return {
            "runs": runs,
            "count": len(runs),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Failed to get MLflow runs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve runs: {str(e)}"
        )


# === Admin Endpoints ===

@app.delete("/events/cache", tags=["Admin"])
def clear_event_cache():
    """Clear the event cache (admin endpoint)"""
    try:
        count = detection_service.clear_cache()
        return {
            "status": "cleared",
            "events_cleared": count,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
