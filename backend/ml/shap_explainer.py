"""
SHAP Explainability Module
Generates local SHAP explanations using TreeExplainer on the XGBoost model.
Provides safe fallback using tree feature importances if SHAP calculation encounters any issue.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
import shap
import logging

logger = logging.getLogger("shap_explainer")


class ShapExplainerService:
    def __init__(self, model, feature_names: List[str]):
        self.model = model
        self.feature_names = feature_names
        self.explainer = None
        self._init_explainer()

    def _init_explainer(self):
        try:
            # TreeExplainer is fast and exact for tree-based ensembles (XGBoost)
            self.explainer = shap.TreeExplainer(self.model)
        except Exception as e:
            logger.warning(f"TreeExplainer initialization warning: {e}. Fallback will be used if needed.")
            self.explainer = None

    def explain_instance(
        self,
        scaled_features: np.ndarray,
        raw_feature_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Generates feature attributions for a single inference instance.
        Returns top risk-increasing factors, top protective factors,
        and full attribution list.
        """
        try:
            if self.explainer is not None:
                shap_values = self.explainer.shap_values(scaled_features)
                # Handle binary classification output formats (single array or list of 2 arrays)
                if isinstance(shap_values, list):
                    values = np.array(shap_values[1][0]) if len(shap_values) > 1 else np.array(shap_values[0][0])
                elif len(shap_values.shape) == 2:
                    values = shap_values[0]
                elif len(shap_values.shape) == 3:
                    values = shap_values[0, :, 1]
                else:
                    values = np.squeeze(shap_values)

                return self._format_shap_output(values, raw_feature_df, is_fallback=False)
        except Exception as e:
            logger.error(f"SHAP explanation failed: {e}. Executing fallback...")

        return self._generate_fallback_explanation(raw_feature_df)

    def _format_shap_output(
        self,
        shap_vals: np.ndarray,
        raw_feature_df: pd.DataFrame,
        is_fallback: bool = False
    ) -> Dict[str, Any]:
        records = []
        raw_row = raw_feature_df.iloc[0]

        for i, feat in enumerate(self.feature_names):
            sv = float(shap_vals[i]) if i < len(shap_vals) else 0.0
            val = float(raw_row.get(feat, 0.0))
            impact_desc = "increases risk" if sv > 0 else ("decreases risk" if sv < 0 else "neutral")

            records.append({
                "feature": feat,
                "value": round(val, 2),
                "shap_value": round(sv, 4),
                "impact": impact_desc,
                "abs_impact": abs(sv)
            })

        # Sort by absolute SHAP impact
        sorted_by_impact = sorted(records, key=lambda x: x["abs_impact"], reverse=True)
        
        # Risk factors (positive SHAP pushing probability higher)
        top_risk_factors = [
            {
                "feature": r["feature"],
                "value": r["value"],
                "shap_value": r["shap_value"],
                "impact": r["impact"]
            }
            for r in sorted_by_impact if r["shap_value"] > 0
        ][:5]

        # Protective factors (negative SHAP pushing probability lower)
        top_protective_factors = [
            {
                "feature": r["feature"],
                "value": r["value"],
                "shap_value": r["shap_value"],
                "impact": r["impact"]
            }
            for r in sorted_by_impact if r["shap_value"] < 0
        ][:5]

        return {
            "is_fallback": is_fallback,
            "method": "SHAP TreeExplainer" if not is_fallback else "Model Feature Importance Fallback",
            "top_risk_factors": top_risk_factors,
            "top_protective_factors": top_protective_factors,
            "all_feature_attributions": sorted_by_impact[:10]
        }

    def _generate_fallback_explanation(self, raw_feature_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Safe heuristic attribution fallback based on feature importances
        and deviation from normal medians.
        """
        raw_row = raw_feature_df.iloc[0]
        records = []

        importances = getattr(self.model, "feature_importances_", None)
        if importances is None:
            importances = np.ones(len(self.feature_names)) / len(self.feature_names)

        # Baseline reference for key risk drivers
        risk_directions = {
            "rainfall_24h": 1,
            "rainfall_7d": 1,
            "rainfall_pressure": 1,
            "slope": 1,
            "slope_risk": 1,
            "soil_moisture": 1,
            "soil_moisture_risk": 1,
            "terrain_instability": 1,
            "ndvi": -1,
            "vegetation_stability": -1,
            "vegetation_index": -1,
            "historical_landslides": 1,
            "previous_landslide": 1,
        }

        for i, feat in enumerate(self.feature_names):
            val = float(raw_row.get(feat, 0.0))
            imp = float(importances[i]) if i < len(importances) else 0.01
            direction = risk_directions.get(feat, 1)
            pseudo_shap = imp * direction * (0.5 if val > 0 else -0.5)

            impact_desc = "increases risk" if pseudo_shap > 0 else "decreases risk"
            records.append({
                "feature": feat,
                "value": round(val, 2),
                "shap_value": round(pseudo_shap, 4),
                "impact": impact_desc,
                "abs_impact": abs(pseudo_shap)
            })

        sorted_records = sorted(records, key=lambda x: x["abs_impact"], reverse=True)
        top_risk = [r for r in sorted_records if r["shap_value"] > 0][:5]
        top_protective = [r for r in sorted_records if r["shap_value"] < 0][:5]

        return {
            "is_fallback": True,
            "method": "Model Feature Importance Fallback (TreeExplainer Fallback)",
            "top_risk_factors": top_risk,
            "top_protective_factors": top_protective,
            "all_feature_attributions": sorted_records[:10]
        }
