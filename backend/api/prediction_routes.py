from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, Any

from backend.api.schemas import EnvironmentalInputSchema
from backend.ml.predict import predictor
from backend.agents.crew import landslide_crew
from backend.ml.evaluate import get_model_evaluation_metrics, get_global_feature_importance
from backend.database import log_prediction
from backend.services.weather_service import recent_weather_service

router = APIRouter(prefix="/api", tags=["Prediction & Analysis"])


@router.post("/predict")
def predict_endpoint(payload: EnvironmentalInputSchema):
    """
    ML Prediction endpoint:
    Performs data sanitization, feature engineering, scaling, XGBoost inference,
    and SHAP explainability.
    """
    try:
        data_dict = payload.model_dump()
        result = predictor.predict(data_dict)
        return {
            "risk_score": result["risk_score"],
            "risk_category": result["risk_category"],
            "probability": result["probability"],
            "risk_color": result["risk_color"],
            "model_used": result["model_used"],
            "shap_explanation": result["shap_explanation"],
            "summary": result["summary"],
            "disclaimer": result["disclaimer"],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/risk-analysis")
def full_risk_analysis_endpoint(payload: EnvironmentalInputSchema):
    """
    Complete Agentic AI Risk Analysis endpoint:
    Runs ML Prediction + SHAP + 4-Agent CrewAI Analysis (Weather, Terrain, Satellite, Risk & Warning).
    """
    try:
        data_dict = payload.model_dump()

        # 1. ML Prediction + SHAP
        ml_result = predictor.predict(data_dict)

        # 2. 4-Agent CrewAI Workflow
        crew_analysis = landslide_crew.kickoff(raw_input=data_dict, ml_prediction=ml_result)

        # 3. Log to SQLite
        log_prediction(data=data_dict, result=ml_result)

        risk_agent_out = crew_analysis["risk_agent"]

        return {
            "risk_score": risk_agent_out["final_risk_score"],
            "risk_category": risk_agent_out["risk_category"],
            "model_probability": ml_result["probability"],
            "risk_color": ml_result["risk_color"],
            "confidence": risk_agent_out["confidence"],
            "warning": risk_agent_out["warning_message"],
            "recommended_action": risk_agent_out["recommended_action"],
            "action_level": risk_agent_out["action_level"],
            "key_factors": risk_agent_out["key_factors"],
            "shap_explanation": ml_result["shap_explanation"],
            "agent_analysis": crew_analysis,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "disclaimer": "DEMO / SIMULATED DATA — Prototype AI evaluation only. Not a live emergency-warning system."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk analysis error: {str(e)}")


@router.post("/risk-forecast")
def risk_forecast_endpoint(payload: EnvironmentalInputSchema):
    """Predict current and next-seven-day landslide risk from weather forecasts."""
    try:
        base_data = payload.model_dump()
        current_prediction = predictor.predict(base_data)
        weather_forecast = recent_weather_service.fetch_forecast_weather(
            payload.latitude, payload.longitude, days=7
        )
        daily = []
        for forecast_day in weather_forecast["forecast"]:
            day_data = {**base_data, **forecast_day}
            # Keep the user/provider's current antecedent rainfall as the lower bound
            # while adding forecast weather for each future day.
            day_data["rainfall_7d"] = max(
                float(base_data.get("rainfall_7d", 0.0)),
                float(forecast_day["rainfall_7d"]),
            )
            prediction = predictor.predict(day_data)
            daily.append({
                "date": forecast_day["date"],
                "risk_score": prediction["risk_score"],
                "risk_category": prediction["risk_category"],
                "probability": prediction["probability"],
                "rainfall_24h": forecast_day["rainfall_24h"],
                "rainfall_7d": day_data["rainfall_7d"],
            })

        highest = max(daily, key=lambda item: item["risk_score"], default=None)
        current_score = current_prediction["risk_score"]
        upcoming_score = highest["risk_score"] if highest else 0
        return {
            "current_risk_yes": current_score >= 25,
            "current_risk_score": current_score,
            "current_probability": current_prediction["probability"],
            "current_category": current_prediction["risk_category"],
            "upcoming_risk_yes": upcoming_score >= 25,
            "upcoming_max_score": upcoming_score,
            "upcoming_max_probability": highest["probability"] if highest else 0,
            "highest_risk_day": highest["date"] if highest else None,
            "highest_risk_category": highest["risk_category"] if highest else "LOW",
            "daily_forecast": daily,
            "weather_source": weather_forecast["source"],
            "disclaimer": weather_forecast["disclaimer"],
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk forecast error: {str(e)}")


@router.get("/model-info")
def model_info_endpoint():
    """
    Returns comparative evaluation metrics and metadata for all models trained on the synthetic dataset.
    """
    try:
        metrics = get_model_evaluation_metrics()
        return {
            "system": "Pure AI Landslide Early Warning Architecture",
            "sensors": "None (Pure Digital Remote Sensing & Environmental Ingestion)",
            "primary_model": "XGBoost Classifier",
            "fallback_model": "Random Forest Classifier",
            "explainability": "SHAP (SHapley Additive exPlanations) TreeExplainer",
            "records_trained": metrics.get("dataset_records", 1500),
            "train_samples": metrics.get("train_samples", 1200),
            "test_samples": metrics.get("test_samples", 300),
            "feature_count": metrics.get("feature_count", 26),
            "models_comparison": metrics.get("models", {}),
            "disclaimer": "DEMO / SIMULATED DATA"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model info retrieval error: {str(e)}")


@router.get("/feature-importance")
def feature_importance_endpoint():
    """
    Returns global feature importance rankings from the primary model.
    """
    try:
        return get_global_feature_importance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature importance error: {str(e)}")
