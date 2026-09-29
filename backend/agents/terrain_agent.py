"""
AGENT 2: TERRAIN & GEOLOGY ANALYST
Responsibilities:
- Analyze elevation profile
- Analyze slope inclination angle (critical threshold > 28-35 degrees)
- Analyze terrain roughness and topographic position
- Analyze planform and profile curvature (concave slopes concentrate water)
- Identify geomorphological failure susceptibility
"""

from typing import Dict, Any, List


class TerrainAgent:
    def __init__(self):
        self.name = "Terrain & Geology Analyst"
        self.role = "Geomorphological Susceptibility Specialist"

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        elevation = float(data.get("elevation", 500.0))
        slope = float(data.get("slope", 15.0))
        aspect = float(data.get("aspect", 180.0))
        terrain_roughness = float(data.get("terrain_roughness", 0.3))
        curvature = float(data.get("curvature", 0.0))
        latitude = float(data.get("latitude", 20.0))
        longitude = float(data.get("longitude", 80.0))

        # Terrain risk scoring (0-100)
        # Slope > 30 is heavily penalized; roughness contributes to shear stress variation
        if slope >= 40.0:
            slope_contrib = 95.0
        elif slope >= 30.0:
            slope_contrib = 65.0 + ((slope - 30.0) / 10.0) * 25.0
        elif slope >= 20.0:
            slope_contrib = 35.0 + ((slope - 20.0) / 10.0) * 30.0
        else:
            slope_contrib = (slope / 20.0) * 35.0

        roughness_contrib = min(100.0, terrain_roughness * 100.0)
        # Concave curvature (positive/negative depending on convention, here non-zero concentrates shear/flow)
        curv_contrib = min(100.0, abs(curvature) * 60.0)
        elev_contrib = min(100.0, (elevation / 3000.0) * 100.0)

        terrain_score = round(
            (slope_contrib * 0.50) +
            (roughness_contrib * 0.25) +
            (curv_contrib * 0.15) +
            (elev_contrib * 0.10),
            1
        )

        factors: List[str] = []
        if slope > 35.0:
            factors.append(f"Precipitous slope angle of {slope:.1f}° exceeds internal friction angle of typical colluvium.")
        elif slope > 25.0:
            factors.append(f"Moderately steep incline of {slope:.1f}° possesses moderate gravitational shear stress.")
        else:
            factors.append(f"Gentle terrain slope ({slope:.1f}°) provides natural gravitational stability.")

        if terrain_roughness > 0.70:
            factors.append(f"High terrain roughness index ({terrain_roughness:.2f}) reflects fractured rock and fragmented talus.")
        elif terrain_roughness > 0.40:
            factors.append(f"Moderate surface roughness ({terrain_roughness:.2f}) indicates uneven hill-slope morphology.")

        if abs(curvature) > 0.50:
            factors.append(f"Significant slope curvature ({curvature:.2f}) acts as a hydro-topographic flow convergent zone.")

        if elevation > 1800.0:
            factors.append(f"High elevation ({elevation:.0f} m) exposed to periglacial weathering and high kinetic energy.")

        if terrain_score >= 75.0:
            risk_level = "CRITICAL"
            summary = (
                f"Severe topographic vulnerability. Steep slope ({slope:.1f}°) and pronounced terrain roughness "
                f"({terrain_roughness:.2f}) indicate extreme gravitational shearing forces prone to rapid mass movement."
            )
        elif terrain_score >= 50.0:
            risk_level = "HIGH"
            summary = (
                f"Elevated topographic susceptibility. The {slope:.1f}° incline combined with broken terrain morphology "
                f"creates localized structural instability."
            )
        elif terrain_score >= 25.0:
            risk_level = "MODERATE"
            summary = f"Moderate terrain slope ({slope:.1f}°). Topography alone is relatively stable but vulnerable if saturated."
        else:
            risk_level = "LOW"
            summary = f"Gentle topography ({slope:.1f}° slope, {elevation:.0f}m elevation). Low gravitational failure potential."

        return {
            "agent_name": self.name,
            "terrain_risk": risk_level,
            "terrain_risk_score": terrain_score,
            "terrain_summary": summary,
            "terrain_factors": factors,
            "metrics": {
                "elevation_m": elevation,
                "slope_deg": slope,
                "aspect_deg": aspect,
                "terrain_roughness": terrain_roughness,
                "curvature": curvature,
                "coordinates": f"{latitude:.4f}, {longitude:.4f}"
            }
        }
