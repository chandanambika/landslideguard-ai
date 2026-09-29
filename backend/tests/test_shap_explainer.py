import pytest
from backend.ml.predict import predictor
from backend.utils.data_generator import generate_single_demo_record


def test_shap_explanation_structure():
    record = generate_single_demo_record("critical")
    result = predictor.predict(record)
    shap_data = result["shap_explanation"]

    assert "top_risk_factors" in shap_data
    assert "top_protective_factors" in shap_data
    assert "method" in shap_data
    assert isinstance(shap_data["top_risk_factors"], list)
    
    if len(shap_data["top_risk_factors"]) > 0:
        factor = shap_data["top_risk_factors"][0]
        assert "feature" in factor
        assert "value" in factor
        assert "shap_value" in factor
        assert factor["shap_value"] > 0
