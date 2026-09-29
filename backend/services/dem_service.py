"""
Mock DEM Service & Topographic Adapter Interface
Simulates digital elevation model (SRTM / ALOS PALSAR) terrain morphometry.
"""

from typing import Dict, Any
import numpy as np


class DEMServiceAdapter:
    """Interface for DEM providers (USGS 3DEP, SRTM 30m, Copernicus DEM, or Mock)."""
    def fetch_terrain(self, lat: float, lon: float) -> Dict[str, Any]:
        raise NotImplementedError


class MockDEMService(DEMServiceAdapter):
    def fetch_terrain(self, lat: float, lon: float) -> Dict[str, Any]:
        # Hash coordinates for stable, repeatable terrain attributes
        np.random.seed(int(abs(lat * 50 + lon * 70)) % 10000)

        elevation = round(float(np.clip(300.0 + (lat * 45.0) + np.random.normal(200.0, 150.0), 100.0, 3800.0)), 1)
        slope = round(float(np.clip(18.0 + (elevation / 120.0) + np.random.normal(5.0, 4.0), 3.0, 58.0)), 1)
        aspect = round(float(np.random.uniform(0.0, 360.0)), 1)
        terrain_roughness = round(float(np.clip(0.25 + (slope / 75.0) + np.random.normal(0, 0.05), 0.10, 0.95)), 2)
        curvature = round(float(np.clip(np.random.normal(0.05, 0.40), -1.5, 1.5)), 2)

        return {
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "elevation": elevation,
            "slope": slope,
            "aspect": aspect,
            "terrain_roughness": terrain_roughness,
            "curvature": curvature,
            "source": "Simulated DEM 30m Service Adapter (Demo Mode)",
            "disclaimer": "DEMO / SIMULATED DATA"
        }


dem_service = MockDEMService()
