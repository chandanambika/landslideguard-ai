import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_and_health():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "online"

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"


def test_demo_data_endpoint():
    resp = client.post("/api/demo-data", json={"hazard_profile": "moderate"})
    assert resp.status_code == 200
    body = resp.json()
    assert "data" in body
    assert "rainfall_24h" in body["data"]


def test_sample_locations_endpoint():
    resp = client.get("/api/sample-locations")
    assert resp.status_code == 200
    body = resp.json()
    assert "locations" in body
    assert len(body["locations"]) >= 4


def test_predict_endpoint():
    payload = {
        "region_name": "Test Escarpment",
        "latitude": 19.5,
        "longitude": 74.5,
        "rainfall_24h": 85.0,
        "rainfall_7d": 220.0,
        "slope": 35.0,
        "soil_moisture": 0.70,
        "ndvi": 0.35,
        "historical_landslides": 2,
        "previous_landslide": 1
    }
    resp = client.post("/api/predict", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "risk_score" in data
    assert "risk_category" in data
    assert "shap_explanation" in data


def test_risk_analysis_endpoint():
    payload = {
        "region_name": "Alpine Ridge Test",
        "latitude": 30.5,
        "longitude": 79.5,
        "rainfall_24h": 110.0,
        "rainfall_7d": 280.0,
        "rainfall_intensity": 16.0,
        "temperature": 18.0,
        "humidity": 85.0,
        "elevation": 1600.0,
        "slope": 38.0,
        "terrain_roughness": 0.75,
        "curvature": 0.45,
        "ndvi": 0.30,
        "ndwi": 0.25,
        "soil_moisture": 0.80,
        "vegetation_index": 0.32,
        "historical_landslides": 3,
        "previous_landslide": 1
    }
    resp = client.post("/api/risk-analysis", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "risk_score" in data
    assert "risk_category" in data
    assert "warning" in data
    assert "agent_analysis" in data
    assert "weather_agent" in data["agent_analysis"]
    assert "terrain_agent" in data["agent_analysis"]
    assert "satellite_agent" in data["agent_analysis"]
    assert "risk_agent" in data["agent_analysis"]


def test_mock_services():
    coords = {"latitude": 18.5, "longitude": 73.8}
    
    w_resp = client.post("/api/weather/mock", json=coords)
    assert w_resp.status_code == 200
    assert "rainfall_24h" in w_resp.json()

    dem_resp = client.post("/api/dem/mock", json=coords)
    assert dem_resp.status_code == 200
    assert "slope" in dem_resp.json()

    sat_resp = client.post("/api/satellite/mock", json=coords)
    assert sat_resp.status_code == 200
    assert "ndvi" in sat_resp.json()


def test_alert_simulation():
    req = {
        "risk_category": "CRITICAL",
        "risk_score": 88.5,
        "location": "Sector Alpha",
        "coordinates": "30.5, 79.5",
        "primary_factors": ["High Rainfall", "Steep Slope"]
    }
    resp = client.post("/api/alerts/simulate", json=req)
    assert resp.status_code == 200
    assert resp.json()["status"] == "Alert Generated Successfully"
