"""
Prediction Service
Loads trained XGBoost model (with Random Forest fallback), Preprocessing Scaler,
and SHAP Explainer. Computes probabilities, maps to 0-100 score, and categorizes risk.
"""

import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import logging

from backend.config import settings
from backend.services.preprocessing_service import PreprocessingService
from backend.ml.shap_explainer import ShapExplainerService
from backend.utils.risk_utils import format_risk_response

logger = logging.getLogger("predict_service")


class Predictor:
    def __init__(self):
        self.preprocessor = PreprocessingService(scaler_path=settings.SCALER_PATH)
        self.xgb_model = None
        self.rf_model = None
        self.shap_service = None
        self.active_model_name = "XGBoost"
        self._load_models()

    def _load_models(self):
        # Load Scaler
        if settings.SCALER_PATH.exists():
            self.preprocessor.load_scaler(settings.SCALER_PATH)

        # Load XGBoost (Primary)
        if settings.XGB_MODEL_PATH.exists():
            try:
                self.xgb_model = joblib.load(settings.XGB_MODEL_PATH)
                self.active_model_name = "XGBoost"
                logger.info("Loaded primary XGBoost model.")
            except Exception as e:
                logger.error(f"Error loading XGBoost model: {e}")

        # Load Random Forest (Fallback)
        if settings.RF_MODEL_PATH.exists():
            try:
                self.rf_model = joblib.load(settings.RF_MODEL_PATH)
                logger.info("Loaded fallback Random Forest model.")
            except Exception as e:
                logger.error(f"Error loading Random Forest model: {e}")

        # Initialize SHAP explainer on primary model
        model_to_explain = self.xgb_model if self.xgb_model is not None else self.rf_model
        if model_to_explain is not None:
            self.shap_service = ShapExplainerService(
                model=model_to_explain,
                feature_names=self.preprocessor.all_feature_names
            )

    def predict(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes end-to-end inference:
        1. Preprocess & engineer features
        2. Scale features
        3. Model probability prediction (XGBoost with RF fallback)
        4. Calculate 0-100 risk score and category
        5. Generate SHAP explanation
        """
        # Ensure models are loaded
        if self.xgb_model is None and self.rf_model is None:
            self._load_models()
            if self.xgb_model is None and self.rf_model is None:
                raise RuntimeError("No trained model available. Please train models first.")

        # Transform features
        scaled_array, raw_feature_df = self.preprocessor.transform_single(raw_input)

        # Model inference
        probability = 0.5
        model_used = "XGBoost"
        try:
            if self.xgb_model is not None:
                prob = self.xgb_model.predict_proba(scaled_array)
                probability = float(prob[0][1])
                model_used = "XGBoost"
            elif self.rf_model is not None:
                prob = self.rf_model.predict_proba(scaled_array)
                probability = float(prob[0][1])
                model_used = "Random Forest (Fallback)"
        except Exception as e:
            logger.warning(f"Inference error on primary model: {e}. Trying fallback...")
            if self.rf_model is not None:
                prob = self.rf_model.predict_proba(scaled_array)
                probability = float(prob[0][1])
                model_used = "Random Forest (Fallback)"
            else:
                raise e

        # Calculate risk score (0-100) & risk category
        risk_data = format_risk_response(probability)

        # SHAP attribution
        shap_explanation = {}
        if self.shap_service is not None:
            try:
                shap_explanation = self.shap_service.explain_instance(scaled_array, raw_feature_df)
            except Exception as e:
                logger.error(f"SHAP explanation exception: {e}")
                shap_explanation = {
                    "is_fallback": True,
                    "method": "Error fallback",
                    "top_risk_factors": [],
                    "top_protective_factors": [],
                    "all_feature_attributions": []
                }

        # Format input summary
        feature_dict = raw_feature_df.iloc[0].to_dict()

        return {
            "risk_score": risk_data["risk_score"],
            "risk_category": risk_data["risk_category"],
            "probability": risk_data["probability"],
            "risk_color": risk_data["color"],
            "model_used": model_used,
            "shap_explanation": shap_explanation,
            "features_used": feature_dict,
            "summary": risk_data["summary"],
            "disclaimer": risk_data["disclaimer"]
        }


# Singleton instance
predictor = Predictor()
