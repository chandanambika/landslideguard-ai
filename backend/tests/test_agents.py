import pytest
from backend.agents.weather_agent import WeatherAgent
from backend.agents.terrain_agent import TerrainAgent
from backend.agents.satellite_agent import SatelliteAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.crew import landslide_crew
from backend.utils.data_generator import generate_single_demo_record
from backend.ml.predict import predictor


def test_weather_agent():
    agent = WeatherAgent()
    sample = {"rainfall_24h": 120.0, "rainfall_7d": 300.0, "humidity": 90.0}
    res = agent.analyze(sample)
    assert res["weather_risk"] in ["HIGH", "CRITICAL"]
    assert "weather_risk_score" in res
    assert len(res["weather_factors"]) > 0


def test_terrain_agent():
    agent = TerrainAgent()
    sample = {"slope": 42.0, "terrain_roughness": 0.8, "elevation": 1500.0}
    res = agent.analyze(sample)
    assert res["terrain_risk"] in ["HIGH", "CRITICAL"]
    assert "terrain_summary" in res


def test_satellite_agent():
    agent = SatelliteAgent()
    sample = {"soil_moisture": 0.85, "ndvi": 0.20, "ndwi": 0.35}
    res = agent.analyze(sample)
    assert res["satellite_risk"] in ["HIGH", "CRITICAL"]
    assert "satellite_summary" in res


def test_crew_orchestration():
    record = generate_single_demo_record("high")
    ml_pred = predictor.predict(record)
    crew_result = landslide_crew.kickoff(record, ml_pred)

    assert "weather_agent" in crew_result
    assert "terrain_agent" in crew_result
    assert "satellite_agent" in crew_result
    assert "risk_agent" in crew_result
    risk_agent = crew_result["risk_agent"]
    assert 0 <= risk_agent["final_risk_score"] <= 100
    assert risk_agent["risk_category"] in ["LOW", "MODERATE", "HIGH", "CRITICAL"]
    assert "action_level" in risk_agent
