import pytest
from backend.ml.predict import predictor
from backend.utils.data_generator import generate_single_demo_record


def test_model_prediction():
    demo_record = generate_single_demo_record("high")
    result = predictor.predict(demo_record)

    assert "risk_score" in result
    assert 0.0 <= result["risk_score"] <= 100.0
    assert result["risk_category"] in ["LOW", "MODERATE", "HIGH", "CRITICAL"]
    assert 0.0 <= result["probability"] <= 1.0
    assert "shap_explanation" in result
    assert "top_risk_factors" in result["shap_explanation"]


def test_prediction_boundary_extremes():
    # Extreme low hazard condition
    low_record = generate_single_demo_record("low")
    low_res = predictor.predict(low_record)
    assert low_res["risk_score"] < 50.0

    # Extreme high hazard condition
    critical_record = generate_single_demo_record("critical")
    critical_res = predictor.predict(critical_record)
    assert critical_res["risk_score"] > 50.0
