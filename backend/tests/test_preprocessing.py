import pytest
import pandas as pd
from backend.services.preprocessing_service import PreprocessingService
from backend.ml.feature_engineering import add_engineered_features, ENGINEERED_FEATURE_NAMES
from backend.utils.risk_utils import calculate_risk_category, format_risk_response


def test_feature_engineering_dict():
    sample = {
        "rainfall_24h": 100.0,
        "rainfall_7d": 250.0,
        "rainfall_intensity": 15.0,
        "humidity": 80.0,
        "slope": 35.0,
        "terrain_roughness": 0.7,
        "curvature": 0.4,
        "soil_moisture": 0.75,
        "ndvi": 0.3,
        "vegetation_index": 0.35,
        "historical_landslides": 2,
        "previous_landslide": 1
    }
    res = add_engineered_features(sample)
    for feat in ENGINEERED_FEATURE_NAMES:
        assert feat in res
    assert res["rainfall_pressure"] == 100.0 * 0.6 + 250.0 * 0.4


def test_preprocessing_service_sanitization():
    preprocessor = PreprocessingService()
    dirty_record = {
        "latitude": 999.0,  # exceeds bounds
        "rainfall_24h": "invalid",
        "slope": -5.0
    }
    sanitized = preprocessor.validate_and_sanitize_record(dirty_record)
    assert sanitized["latitude"] == 90.0
    assert sanitized["rainfall_24h"] == 10.0  # default fallback
    assert sanitized["slope"] == 0.0


def test_risk_categorization():
    cat, color, _ = calculate_risk_category(15.0)
    assert cat == "LOW"
    cat, color, _ = calculate_risk_category(35.0)
    assert cat == "MODERATE"
    cat, color, _ = calculate_risk_category(60.0)
    assert cat == "HIGH"
    cat, color, _ = calculate_risk_category(85.0)
    assert cat == "CRITICAL"

    resp = format_risk_response(0.82)
    assert resp["risk_score"] == 82.0
    assert resp["risk_category"] == "CRITICAL"
