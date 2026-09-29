"""
Mock Satellite & Remote Sensing Service Adapter
Simulates Sentinel-2 / Landsat-8 multispectral and SMAP soil moisture data.
"""

from typing import Dict, Any
import numpy as np


class SatelliteServiceAdapter:
    """Interface for Satellite imagery & bio-physical proxy providers."""
    def fetch_remote_sensing(self, lat: float, lon: float) -> Dict[str, Any]:
        raise NotImplementedError


class MockSatelliteService(SatelliteServiceAdapter):
    def fetch_remote_sensing(self, lat: float, lon: float) -> Dict[str, Any]:
        np.random.seed(int(abs(lat * 80 + lon * 30)) % 10000)

        ndvi = round(float(np.clip(np.random.beta(3.5, 2.5), 0.10, 0.88)), 2)
        ndwi = round(float(np.clip(np.random.uniform(-0.35, 0.45), -0.40, 0.50)), 2)
        # Soil moisture proxy correlates inversely with extreme dry indices and positively with NDWI
        soil_moisture = round(float(np.clip(0.40 + (ndwi * 0.45) + np.random.normal(0.05, 0.08), 0.15, 0.95)), 2)
        vegetation_index = round(float(np.clip(ndvi + np.random.normal(0, 0.03), 0.10, 0.90)), 2)
        land_cover = "Evergreen Forest" if ndvi > 0.65 else ("Shrubland / Colluvial Slope" if ndvi > 0.35 else "Exposed Rock / Degraded Soil")

        return {
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "ndvi": ndvi,
            "ndwi": ndwi,
            "soil_moisture": soil_moisture,
            "vegetation_index": vegetation_index,
            "land_cover": land_cover,
            "sensor": "Simulated Sentinel-2 MSI / SMAP L4",
            "source": "Mock Remote Sensing Service (Demo Mode)",
            "disclaimer": "DEMO / SIMULATED DATA"
        }


satellite_service = MockSatelliteService()
