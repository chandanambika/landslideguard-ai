"""
AGENT 3: SATELLITE & VEGETATION ANALYST
Responsibilities:
- Analyze NDVI (Vegetation density and root cohesion)
- Analyze NDWI (Surface water and canopy water content)
- Analyze soil moisture proxy (subsurface saturation level)
- Analyze vegetation stability metrics
- Detect deforested, exposed, or waterlogged surfaces
"""

from typing import Dict, Any, List


class SatelliteAgent:
    def __init__(self):
        self.name = "Satellite & Vegetation Analyst"
        self.role = "Remote Sensing & Bio-Physical Specialist"

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        ndvi = float(data.get("ndvi", 0.5))
        ndwi = float(data.get("ndwi", 0.0))
        soil_moisture = float(data.get("soil_moisture", 0.4))
        vegetation_index = float(data.get("vegetation_index", 0.5))

        # Satellite risk scoring (0-100)
        # High soil moisture + high NDWI + low NDVI = highest danger
        soil_contrib = min(100.0, soil_moisture * 100.0)
        ndwi_contrib = max(0.0, min(100.0, (ndwi + 0.3) * 110.0))
        # Low NDVI means lack of tree roots to anchor colluvial mantle
        ndvi_danger = max(0.0, min(100.0, (0.75 - ndvi) * 133.0))

        satellite_score = round(
            (soil_contrib * 0.45) +
            (ndvi_danger * 0.35) +
            (ndwi_contrib * 0.20),
            1
        )

        factors: List[str] = []
        if soil_moisture > 0.75:
            factors.append(f"Near-saturated subsurface soil moisture ({soil_moisture * 100:.1f}%) eliminates matric suction.")
        elif soil_moisture > 0.50:
            factors.append(f"Elevated soil moisture ({soil_moisture * 100:.1f}%) indicates reduced soil shear strength.")
        else:
            factors.append(f"Low soil moisture ({soil_moisture * 100:.1f}%) maintains positive capillary soil tension.")

        if ndvi < 0.30:
            factors.append(f"Sparse vegetation cover (NDVI: {ndvi:.2f}) provides deficient root reinforcement.")
        elif ndvi > 0.60:
            factors.append(f"Dense vegetative canopy (NDVI: {ndvi:.2f}) affords substantial root anchoring and rainfall interception.")
        else:
            factors.append(f"Moderate vegetation cover (NDVI: {ndvi:.2f}) provides intermediate slope protection.")

        if ndwi > 0.20:
            factors.append(f"Elevated surface water index (NDWI: {ndwi:.2f}) confirms active surface pooling and runoff.")

        if satellite_score >= 75.0:
            risk_level = "CRITICAL"
            summary = (
                f"Severe bio-physical hazard detected via multispectral proxies. Critically elevated soil moisture "
                f"({soil_moisture * 100:.0f}%) coupled with degraded vegetative cover (NDVI: {ndvi:.2f}) produces acute liquefaction potential."
            )
        elif satellite_score >= 50.0:
            risk_level = "HIGH"
            summary = (
                f"High remote-sensing hazard signature. Soil is substantially saturated ({soil_moisture * 100:.0f}%) with "
                f"insufficient vegetative root networks to prevent planar slipping."
            )
        elif satellite_score >= 25.0:
            risk_level = "MODERATE"
            summary = (
                f"Moderate moisture loading observed (Soil moisture: {soil_moisture * 100:.0f}%, NDVI: {ndvi:.2f}). "
                f"Vegetation provides partial protective stabilization."
            )
        else:
            risk_level = "LOW"
            summary = f"Healthy vegetation cover (NDVI: {ndvi:.2f}) and dry-to-moderate soil moisture ({soil_moisture * 100:.0f}%) stabilize ground layers."

        return {
            "agent_name": self.name,
            "satellite_risk": risk_level,
            "satellite_risk_score": satellite_score,
            "satellite_summary": summary,
            "satellite_factors": factors,
            "metrics": {
                "ndvi": ndvi,
                "ndwi": ndwi,
                "soil_moisture": soil_moisture,
                "vegetation_index": vegetation_index
            }
        }
