from fastapi import APIRouter, Query
from typing import Dict, Any, List

from backend.api.schemas import CoordinateQuery, DemoDataRequest, AlertSimulationRequest
from backend.utils.data_generator import generate_single_demo_record
from backend.services.weather_service import weather_service, recent_weather_service
from backend.services.dem_service import dem_service
from backend.services.satellite_service import satellite_service
from backend.services.alert_service import alert_service
from backend.database import get_recent_alerts

router = APIRouter(prefix="/api", tags=["Data & Mock Services"])


PREDEFINED_LOCATIONS = [
    {
        "id": "hill_region",
        "name": "Hill Region Demo",
        "description": "Rolling hills with moderate inclination, typical monsoon rains, and partial tree cover.",
        "hazard_profile": "moderate",
        "latitude": 18.5204,
        "longitude": 73.8567,
        "data": {
            "region_name": "Western Ghats Escarpment",
            "latitude": 18.5204,
            "longitude": 73.8567,
            "elevation": 920.0,
            "slope": 26.5,
            "aspect": 210.0,
            "terrain_roughness": 0.48,
            "curvature": -0.22,
            "rainfall_24h": 68.5,
            "rainfall_7d": 185.0,
            "rainfall_intensity": 11.2,
            "temperature": 23.4,
            "humidity": 78.0,
            "wind_speed": 16.5,
            "ndvi": 0.46,
            "ndwi": 0.12,
            "soil_moisture": 0.62,
            "vegetation_index": 0.48,
            "historical_landslides": 1,
            "previous_landslide": 0
        }
    },
    {
        "id": "mountain_region",
        "name": "Mountain Region Demo",
        "description": "Rugged alpine terrain with precipitous slopes and fractured bedrock.",
        "hazard_profile": "high",
        "latitude": 30.1450,
        "longitude": 79.2310,
        "data": {
            "region_name": "Garhwal Himalayan Ridge",
            "latitude": 30.1450,
            "longitude": 79.2310,
            "elevation": 2150.0,
            "slope": 38.2,
            "aspect": 175.0,
            "terrain_roughness": 0.76,
            "curvature": 0.54,
            "rainfall_24h": 95.0,
            "rainfall_7d": 260.0,
            "rainfall_intensity": 18.5,
            "temperature": 16.2,
            "humidity": 86.0,
            "wind_speed": 26.0,
            "ndvi": 0.32,
            "ndwi": 0.22,
            "soil_moisture": 0.74,
            "vegetation_index": 0.34,
            "historical_landslides": 3,
            "previous_landslide": 1
        }
    },
    {
        "id": "high_rainfall",
        "name": "High Rainfall Demo (Critical)",
        "description": "Extreme torrential rainfall event over saturated steep slopes.",
        "hazard_profile": "critical",
        "latitude": 25.2700,
        "longitude": 91.7300,
        "data": {
            "region_name": "Cherrapunji / Khasi Hills Sector",
            "latitude": 25.2700,
            "longitude": 91.7300,
            "elevation": 1430.0,
            "slope": 42.0,
            "aspect": 160.0,
            "terrain_roughness": 0.84,
            "curvature": 0.85,
            "rainfall_24h": 185.0,
            "rainfall_7d": 440.0,
            "rainfall_intensity": 34.0,
            "temperature": 18.0,
            "humidity": 96.0,
            "wind_speed": 38.0,
            "ndvi": 0.24,
            "ndwi": 0.38,
            "soil_moisture": 0.92,
            "vegetation_index": 0.26,
            "historical_landslides": 5,
            "previous_landslide": 1
        }
    },
    {
        "id": "low_risk",
        "name": "Low Risk Demo",
        "description": "Gentle alluvial valley with thick vegetation cover and minimal antecedent rain.",
        "hazard_profile": "low",
        "latitude": 22.3000,
        "longitude": 73.1800,
        "data": {
            "region_name": "Plains Foothills Valley",
            "latitude": 22.3000,
            "longitude": 73.1800,
            "elevation": 320.0,
            "slope": 8.5,
            "aspect": 95.0,
            "terrain_roughness": 0.18,
            "curvature": 0.02,
            "rainfall_24h": 8.0,
            "rainfall_7d": 25.0,
            "rainfall_intensity": 2.0,
            "temperature": 27.5,
            "humidity": 52.0,
            "wind_speed": 8.5,
            "ndvi": 0.72,
            "ndwi": -0.15,
            "soil_moisture": 0.28,
            "vegetation_index": 0.74,
            "historical_landslides": 0,
            "previous_landslide": 0
        }
    }
]


@router.post("/demo-data")
def get_demo_data(payload: DemoDataRequest = DemoDataRequest()):
    """
    Generates realistic environmental values matching the requested hazard profile.
    """
    record = generate_single_demo_record(payload.hazard_profile)
    return {
        "status": "success",
        "hazard_profile": payload.hazard_profile,
        "data": record,
        "disclaimer": "DEMO / SIMULATED DATA"
    }


@router.get("/sample-locations")
def get_sample_locations():
    """
    Returns predefined benchmark locations representing various risk profiles.
    """
    return {
        "count": len(PREDEFINED_LOCATIONS),
        "locations": PREDEFINED_LOCATIONS,
        "disclaimer": "DEMO / SIMULATED DATA"
    }


@router.post("/weather/mock")
def mock_weather_endpoint(coords: CoordinateQuery):
    """
    Simulated Weather API endpoint.
    """
    return weather_service.fetch_weather(coords.latitude, coords.longitude)


@router.post("/weather/recent")
def recent_weather_endpoint(coords: CoordinateQuery):
    """Fetch recent hourly weather for a location, with an offline demo fallback."""
    return recent_weather_service.fetch_recent_weather(coords.latitude, coords.longitude)


@router.get("/locations/search")
def search_locations(q: str = Query(..., min_length=2, max_length=80)):
    """Search cities using Open-Meteo's free geocoding service."""
    import httpx

    try:
        response = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": q, "count": 6, "language": "en", "format": "json"},
            timeout=8.0,
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        return {
            "results": [
                {
                    "id": result.get("id"),
                    "name": result.get("name"),
                    "admin1": result.get("admin1"),
                    "country": result.get("country"),
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude"),
                }
                for result in results
            ]
        }
    except (httpx.HTTPError, ValueError) as exc:
        return {"results": [], "error": f"City search unavailable: {exc}"}


@router.post("/dem/mock")
def mock_dem_endpoint(coords: CoordinateQuery):
    """
    Simulated Digital Elevation Model (DEM) endpoint.
    """
    return dem_service.fetch_terrain(coords.latitude, coords.longitude)


@router.post("/satellite/mock")
def mock_satellite_endpoint(coords: CoordinateQuery):
    """
    Simulated Multispectral Satellite Remote Sensing endpoint.
    """
    return satellite_service.fetch_remote_sensing(coords.latitude, coords.longitude)


@router.post("/alerts/simulate")
def simulate_alert_endpoint(req: AlertSimulationRequest):
    """
    Simulates early warning dispatch and records in database.
    """
    result = alert_service.trigger_simulated_alert(
        risk_category=req.risk_category,
        risk_score=req.risk_score,
        location=req.location,
        coordinates=req.coordinates,
        primary_factors=req.primary_factors
    )
    return result


@router.get("/alerts/recent")
def get_recent_alerts_endpoint():
    """
    Returns recent simulated alert dispatches.
    """
    return {
        "recent_alerts": get_recent_alerts(10),
        "disclaimer": "DEMO / SIMULATED DATA"
    }
