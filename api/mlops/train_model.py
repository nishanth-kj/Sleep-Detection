"""
MLOps training script for drowsiness detection model
"""
import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_synthetic_data(n_samples=1000):
    """Generate synthetic drowsiness detection data"""
    np.random.seed(42)
    
    # Features: EAR, variance, duration, time_of_day
    X = np.random.rand(n_samples, 4)
    
    # Labels: 0 = awake, 1 = drowsy
    # Drowsy if EAR < 0.25 AND duration > 0.5
    y = ((X[:, 0] < 0.25) & (X[:, 2] > 0.5)).astype(int)
    
    return X, y


def train_model():
    """Train a drowsiness detection model"""
    logger.info("Starting model training...")
    
    # Set MLflow tracking URI
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
    mlflow.set_tracking_uri(mlflow_uri)
    
    # Set experiment
    experiment_name = "drowsiness_model_training"
    try:
        mlflow.create_experiment(experiment_name)
    except:
        pass
    mlflow.set_experiment(experiment_name)
    
    # Generate data
    logger.info("Generating synthetic training data...")
    X, y = generate_synthetic_data(n_samples=2000)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Start MLflow run
    with mlflow.start_run(run_name="random_forest_baseline"):
        # Model parameters
        params = {
            "n_estimators": 100,
            "max_depth": 10,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "random_state": 42
        }
        
        # Log parameters
        mlflow.log_params(params)
        
        # Train model
        logger.info("Training Random Forest model...")
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        
        logger.info(f"Model Metrics:")
        logger.info(f"  Accuracy:  {accuracy:.4f}")
        logger.info(f"  Precision: {precision:.4f}")
        logger.info(f"  Recall:    {recall:.4f}")
        logger.info(f"  F1-Score:  {f1:.4f}")
        
        # Log model
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name="drowsiness_detector"
        )
        
        logger.info("Model training completed successfully!")
        
        return model, {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        }


if __name__ == "__main__":
    try:
        model, metrics = train_model()
        logger.info("Training pipeline finished successfully")
    except Exception as e:
        logger.error(f"Training failed: {e}", exc_info=True)
        raise
