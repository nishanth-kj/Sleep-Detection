"""SQLAlchemy database models"""
from sqlalchemy import Column, Integer, Float, Boolean, String, DateTime, JSON
from sqlalchemy.sql import func

from .database import Base


class DetectionEventDB(Base):
    """Detection events table"""
    __tablename__ = "detection_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=func.now(), index=True)
    ear_value = Column(Float, nullable=False)
    is_drowsy = Column(Boolean, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    severity = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "ear_value": self.ear_value,
            "is_drowsy": self.is_drowsy,
            "duration_ms": self.duration_ms,
            "severity": self.severity,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class ModelMetricsDB(Base):
    """Model metrics table"""
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=func.now(), index=True)
    model_name = Column(String(100), default="drowsiness_detector")
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=True)
    additional_metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "model_name": self.model_name,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "additional_metrics": self.additional_metrics,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class SystemEventDB(Base):
    """System events table"""
    __tablename__ = "system_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=func.now(), index=True)
    event_type = Column(String(50), nullable=False, index=True)
    severity = Column(String(20), nullable=False)
    message = Column(String(500), nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "event_type": self.event_type,
            "severity": self.severity,
            "message": self.message,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class UserSessionDB(Base):
    """User sessions table"""
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, nullable=True)
    total_events = Column(Integer, default=0)
    drowsy_events = Column(Integer, default=0)
    average_ear = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_events": self.total_events,
            "drowsy_events": self.drowsy_events,
            "average_ear": self.average_ear,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
