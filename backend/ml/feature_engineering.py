"""
PROTOTYPE / DEMO FEATURE ENGINEERING
Note: The derived feature formulas below are mathematical heuristic approximations
designed for academic prototype demonstration and are NOT scientifically validated geological criteria.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Union


ENGINEERED_FEATURE_NAMES = [
    "rainfall_pressure",
    "rainfall_accumulation",
    "rainfall_intensity_score",
    "slope_risk",
    "soil_moisture_risk",
    "terrain_instability",
    "vegetation_stability",
    "historical_risk",
]


def add_engineered_features(data: Union[pd.DataFrame, Dict[str, Any]]) -> Union[pd.DataFrame, Dict[str, Any]]:
    """
    Computes derived environmental and topographical risk features.
    Accepts either a pandas DataFrame or a dictionary of inputs.
    """
    if isinstance(data, pd.DataFrame):
        df = data.copy()
        
        # Rainfall features
        df["rainfall_pressure"] = df["rainfall_24h"] * 0.6 + df["rainfall_7d"] * 0.4
        df["rainfall_accumulation"] = df["rainfall_24h"] + df["rainfall_7d"]
        df["rainfall_intensity_score"] = df["rainfall_intensity"] * (df["humidity"] / 100.0)
        
        # Slope & Terrain features
        # Critical slope threshold commonly starts around 25-30 degrees in geotechnical literature
        df["slope_risk"] = np.clip(
            np.where(df["slope"] > 28.0, 0.5 + (df["slope"] - 28.0) / 40.0, df["slope"] / 56.0),
            0.0, 1.0
        )
        df["terrain_instability"] = (
            (df["slope"] * 0.5) +
            (df["terrain_roughness"] * 30.0) +
            (np.abs(df["curvature"]) * 20.0)
        )
        
        # Remote Sensing / Soil features
        # Higher soil moisture combined with low vegetative canopy represents high destabilization risk
        df["soil_moisture_risk"] = np.clip(
            df["soil_moisture"] * (1.0 - (df["ndvi"] * 0.5)),
            0.0, 1.0
        )
        df["vegetation_stability"] = (df["ndvi"] * 0.6) + (df["vegetation_index"] * 0.4)
        
        # Historical event risk weighting
        df["historical_risk"] = (df["historical_landslides"] * 10.0) + (df["previous_landslide"] * 25.0)
        
        return df
    
    elif isinstance(data, dict):
        d = dict(data)
        r24 = float(d.get("rainfall_24h", 0.0))
        r7 = float(d.get("rainfall_7d", 0.0))
        r_int = float(d.get("rainfall_intensity", 0.0))
        hum = float(d.get("humidity", 50.0))
        slope = float(d.get("slope", 0.0))
        roughness = float(d.get("terrain_roughness", 0.0))
        curvature = float(d.get("curvature", 0.0))
        soil_m = float(d.get("soil_moisture", 0.0))
        ndvi = float(d.get("ndvi", 0.0))
        veg_idx = float(d.get("vegetation_index", 0.0))
        hist_count = float(d.get("historical_landslides", 0.0))
        prev_landslide = float(d.get("previous_landslide", 0.0))

        slope_r = min(1.0, max(0.0, 0.5 + (slope - 28.0) / 40.0 if slope > 28.0 else slope / 56.0))

        d["rainfall_pressure"] = round(r24 * 0.6 + r7 * 0.4, 3)
        d["rainfall_accumulation"] = round(r24 + r7, 3)
        d["rainfall_intensity_score"] = round(r_int * (hum / 100.0), 3)
        d["slope_risk"] = round(slope_r, 4)
        d["soil_moisture_risk"] = round(min(1.0, max(0.0, soil_m * (1.0 - (ndvi * 0.5)))), 4)
        d["terrain_instability"] = round((slope * 0.5) + (roughness * 30.0) + (abs(curvature) * 20.0), 3)
        d["vegetation_stability"] = round((ndvi * 0.6) + (veg_idx * 0.4), 4)
        d["historical_risk"] = round((hist_count * 10.0) + (prev_landslide * 25.0), 2)
        return d
    
    else:
        raise TypeError("Input must be a pandas DataFrame or a dictionary.")
