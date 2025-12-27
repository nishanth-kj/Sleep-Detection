"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SeverityLevel(str, Enum):
    """Drowsiness severity levels"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DetectionEvent(BaseModel):
    """Model for a single drowsiness detection event"""
    timestamp: Optional[str] = Field(default=None, description="ISO format timestamp")
    ear_value: float = Field(..., ge=0.0, le=1.0, description="Eye Aspect Ratio (0-1)")
    is_drowsy: bool = Field(..., description="Whether drowsiness was detected")
    duration_ms: int = Field(..., ge=0, description="Duration in milliseconds")
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        return v or datetime.utcnow().isoformat()
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2025-12-27T12:00:00.000Z",
                "ear_value": 0.15,
                "is_drowsy": True,
                "duration_ms": 3500
            }
        }


class DetectionResponse(BaseModel):
    """Response after logging a detection event"""
    status: str
    event_id: str
    timestamp: str
    severity: str


class ModelMetrics(BaseModel):
    """Model performance metrics"""
    accuracy: float = Field(..., ge=0.0, le=1.0)
    precision: float = Field(..., ge=0.0, le=1.0)
    recall: float = Field(..., ge=0.0, le=1.0)
    f1_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "accuracy": 0.95,
                "precision": 0.92,
                "recall": 0.94,
                "f1_score": 0.93
            }
        }


class BatchDetectionRequest(BaseModel):
    """Request for logging multiple detection events"""
    events: List[DetectionEvent] = Field(..., min_length=1, max_length=100)


class StatisticsResponse(BaseModel):
    """Response with detection statistics"""
    total_events: int
    drowsy_events: int
    average_ear: float
    average_duration_ms: float
    drowsiness_rate: float
    severity_distribution: Dict[str, int]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    mlflow_uri: str
    timestamp: str
    uptime_seconds: Optional[float] = None


class DashboardSummary(BaseModel):
    """Comprehensive dashboard data"""
    overall: Dict[str, Any]
    last_hour: Dict[str, Any]
    status: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    status_code: int
    timestamp: str
