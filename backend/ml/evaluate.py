"""
Model Evaluation and Metrics Inspection Service
Reads stored metrics or evaluates on demand.
"""

import json
from pathlib import Path
from typing import Dict, Any
from backend.config import settings


def get_model_evaluation_metrics() -> Dict[str, Any]:
    """
    Returns comparative evaluation metrics for Logistic Regression, Random Forest, and XGBoost.
    If the metrics file does not exist, triggers training.
    """
    if not settings.METRICS_PATH.exists() or not settings.XGB_MODEL_PATH.exists():
        from backend.ml.train_model import train_and_evaluate_all
        return train_and_evaluate_all()
    
    with open(settings.METRICS_PATH, "r") as f:
        return json.load(f)


def get_global_feature_importance() -> Dict[str, Any]:
    """
    Returns global feature importance from the primary XGBoost model.
    """
    import joblib
    metrics = get_model_evaluation_metrics()
    feature_names = metrics.get("features", [])

    if settings.XGB_MODEL_PATH.exists():
        model = joblib.load(settings.XGB_MODEL_PATH)
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            sorted_idx = importances.argsort()[::-1]
            return {
                "model": "XGBoost",
                "feature_importances": [
                    {
                        "feature": feature_names[i] if i < len(feature_names) else f"feature_{i}",
                        "importance": round(float(importances[i]), 4)
                    }
                    for i in sorted_idx[:12]
                ]
            }

    return {"model": "Fallback", "feature_importances": []}
