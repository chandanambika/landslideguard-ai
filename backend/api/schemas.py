from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class EnvironmentalInputSchema(BaseModel):
    region_name: Optional[str] = Field(default="Monitored Sector", description="Human-readable sector name")
    latitude: float = Field(default=20.0, ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(default=80.0, ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    
    # Weather
    rainfall_24h: float = Field(default=25.0, ge=0.0, le=1000.0, description="Rainfall in last 24 hours (mm)")
    rainfall_7d: float = Field(default=75.0, ge=0.0, le=3000.0, description="Cumulative rainfall in last 7 days (mm)")
    rainfall_intensity: Optional[float] = Field(default=5.0, ge=0.0, le=200.0, description="Precipitation intensity (mm/h)")
    temperature: Optional[float] = Field(default=24.0, ge=-40.0, le=60.0, description="Ambient surface temperature (°C)")
    humidity: Optional[float] = Field(default=70.0, ge=0.0, le=100.0, description="Relative humidity (%)")
    wind_speed: Optional[float] = Field(default=12.0, ge=0.0, le=200.0, description="Surface wind speed (km/h)")
    
    # Terrain / DEM
    elevation: Optional[float] = Field(default=750.0, ge=-100.0, le=9000.0, description="Digital elevation above sea level (m)")
    slope: float = Field(default=22.0, ge=0.0, le=90.0, description="Terrain slope inclination (degrees)")
    aspect: Optional[float] = Field(default=180.0, ge=0.0, le=360.0, description="Slope azimuth aspect (degrees)")
    terrain_roughness: Optional[float] = Field(default=0.45, ge=0.0, le=2.0, description="Surface topographic roughness index")
    curvature: Optional[float] = Field(default=0.0, ge=-5.0, le=5.0, description="Plan/profile topographic curvature")
    
    # Satellite / Remote Sensing
    ndvi: Optional[float] = Field(default=0.52, ge=-1.0, le=1.0, description="Normalized Difference Vegetation Index")
    ndwi: Optional[float] = Field(default=0.05, ge=-1.0, le=1.0, description="Normalized Difference Water Index")
    soil_moisture: float = Field(default=0.48, ge=0.0, le=1.0, description="Volumetric soil moisture fraction (0.0 to 1.0)")
    vegetation_index: Optional[float] = Field(default=0.50, ge=-1.0, le=1.0, description="Enhanced/Normalized vegetation index")
    
    # Historical
    historical_landslides: Optional[int] = Field(default=1, ge=0, le=100, description="Count of historical landslides in area")
    previous_landslide: Optional[int] = Field(default=0, ge=0, le=1, description="Binary flag indicating prior event")


class CoordinateQuery(BaseModel):
    latitude: float = Field(ge=-90.0, le=90.0)
    longitude: float = Field(ge=-180.0, le=180.0)


class DemoDataRequest(BaseModel):
    hazard_profile: Optional[str] = Field(default="random", description="low, moderate, high, critical, or random")


class AlertSimulationRequest(BaseModel):
    risk_category: str
    risk_score: float
    location: str
    coordinates: str
    primary_factors: List[str] = []
