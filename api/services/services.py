"""
Service layer for drowsiness detection telemetry and ML operations
"""
import mlflow
import mlflow.sklearn
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class MLflowService:
    """Service for MLflow operations"""
    
    def __init__(self, tracking_uri: str = "sqlite:///mlflow.db"):
        self.tracking_uri = tracking_uri
        mlflow.set_tracking_uri(tracking_uri)
        self.experiment_name = "drowsiness_detection"
        
        # Create experiment if it doesn't exist
        try:
            self.experiment_id = mlflow.create_experiment(self.experiment_name)
        except:
            self.experiment_id = mlflow.get_experiment_by_name(self.experiment_name).experiment_id
    
    def log_detection_event(
        self,
        ear_value: float,
        is_drowsy: bool,
        duration_ms: int,
        timestamp: str
    ) -> str:
        """Log a single drowsiness detection event"""
        try:
            with mlflow.start_run(experiment_id=self.experiment_id, run_name=f"detection_{timestamp}"):
                mlflow.log_param("timestamp", timestamp)
                mlflow.log_metric("ear_value", ear_value)
                mlflow.log_metric("is_drowsy", 1 if is_drowsy else 0)
                mlflow.log_metric("duration_ms", duration_ms)
                
                run = mlflow.active_run()
                return run.info.run_id
        except Exception as e:
            logger.error(f"Failed to log detection event: {e}")
            raise
    
    def log_model_metrics(
        self,
        accuracy: float,
        precision: float,
        recall: float,
        f1_score: Optional[float] = None
    ) -> str:
        """Log model performance metrics"""
        try:
            with mlflow.start_run(experiment_id=self.experiment_id, run_name="model_evaluation"):
                mlflow.log_metric("accuracy", accuracy)
                mlflow.log_metric("precision", precision)
                mlflow.log_metric("recall", recall)
                if f1_score:
                    mlflow.log_metric("f1_score", f1_score)
                
                run = mlflow.active_run()
                return run.info.run_id
        except Exception as e:
            logger.error(f"Failed to log model metrics: {e}")
            raise
    
    def get_recent_runs(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get recent MLflow runs"""
        try:
            runs = mlflow.search_runs(
                experiment_ids=[self.experiment_id],
                max_results=max_results,
                order_by=["start_time DESC"]
            )
            return runs.to_dict('records') if not runs.empty else []
        except Exception as e:
            logger.error(f"Failed to get recent runs: {e}")
            return []


class DetectionService:
    """Service for processing detection data"""
    
    def __init__(self):
        self.events_cache: List[Dict[str, Any]] = []
        self.max_cache_size = 1000
    
    def process_detection_event(
        self,
        ear_value: float,
        is_drowsy: bool,
        duration_ms: int,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process and validate a detection event"""
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat()
        
        event = {
            "timestamp": timestamp,
            "ear_value": ear_value,
            "is_drowsy": is_drowsy,
            "duration_ms": duration_ms,
            "severity": self._calculate_severity(ear_value, duration_ms)
        }
        
        # Add to cache
        self.events_cache.append(event)
        if len(self.events_cache) > self.max_cache_size:
            self.events_cache.pop(0)
        
        return event
    
    def _calculate_severity(self, ear_value: float, duration_ms: int) -> str:
        """Calculate drowsiness severity"""
        if ear_value > 0.25:
            return "none"
        elif duration_ms < 2000:
            return "low"
        elif duration_ms < 5000:
            return "medium"
        else:
            return "high"
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics from cached events"""
        if not self.events_cache:
            return {
                "total_events": 0,
                "drowsy_events": 0,
                "average_ear": 0.0,
                "average_duration": 0.0,
                "severity_distribution": {}
            }
        
        total = len(self.events_cache)
        drowsy = sum(1 for e in self.events_cache if e["is_drowsy"])
        avg_ear = sum(e["ear_value"] for e in self.events_cache) / total
        avg_duration = sum(e["duration_ms"] for e in self.events_cache) / total
        
        severity_counts = {}
        for event in self.events_cache:
            severity = event["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            "total_events": total,
            "drowsy_events": drowsy,
            "average_ear": round(avg_ear, 3),
            "average_duration_ms": round(avg_duration, 2),
            "severity_distribution": severity_counts,
            "drowsiness_rate": round(drowsy / total * 100, 2) if total > 0 else 0
        }
    
    def get_recent_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent events from cache"""
        return self.events_cache[-limit:] if self.events_cache else []
    
    def clear_cache(self) -> int:
        """Clear event cache and return number of events cleared"""
        count = len(self.events_cache)
        self.events_cache.clear()
        return count


class AnalyticsService:
    """Service for analytics and insights"""
    
    def __init__(self, detection_service: DetectionService):
        self.detection_service = detection_service
    
    def get_hourly_summary(self) -> Dict[str, Any]:
        """Get summary of last hour's activity"""
        events = self.detection_service.events_cache
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(hours=1)
        
        recent = [
            e for e in events
            if datetime.fromisoformat(e["timestamp"]) > one_hour_ago
        ]
        
        if not recent:
            return {"events_count": 0, "period": "last_hour"}
        
        drowsy_count = sum(1 for e in recent if e["is_drowsy"])
        avg_ear = sum(e["ear_value"] for e in recent) / len(recent)
        
        return {
            "period": "last_hour",
            "events_count": len(recent),
            "drowsy_count": drowsy_count,
            "average_ear": round(avg_ear, 3),
            "alert_rate": round(drowsy_count / len(recent) * 100, 2) if recent else 0
        }
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get comprehensive dashboard summary"""
        stats = self.detection_service.get_statistics()
        hourly = self.get_hourly_summary()
        
        return {
            "overall": stats,
            "last_hour": hourly,
            "status": self._get_system_status(stats),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _get_system_status(self, stats: Dict[str, Any]) -> str:
        """Determine overall system status"""
        if stats["total_events"] == 0:
            return "idle"
        
        drowsiness_rate = stats.get("drowsiness_rate", 0)
        if drowsiness_rate > 50:
            return "critical"
        elif drowsiness_rate > 25:
            return "warning"
        else:
            return "normal"
