import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional

FEATURE_COLUMNS = [
    "latitude",
    "longitude",
    "rainfall_24h",
    "rainfall_7d",
    "rainfall_intensity",
    "temperature",
    "humidity",
    "elevation",
    "slope",
    "aspect",
    "terrain_roughness",
    "curvature",
    "ndvi",
    "ndwi",
    "soil_moisture",
    "vegetation_index",
    "historical_landslides",
    "previous_landslide",
]

TARGET_COLUMN = "landslide"


def generate_synthetic_dataset(
    n_samples: int = 1500,
    random_seed: int = 42,
    output_path: Optional[Path] = None
) -> pd.DataFrame:
    """
    Generates a realistic synthetic dataset for landslide risk prediction.
    Uses physical domain heuristics combined with realistic variance and noise.
    """
    np.random.seed(random_seed)

    # Geographic coordinates (representative of landslide-prone mountainous/hilly belts)
    latitude = np.random.uniform(10.0, 35.0, n_samples)
    longitude = np.random.uniform(70.0, 95.0, n_samples)

    # Weather variables
    rainfall_24h = np.random.exponential(scale=35.0, size=n_samples)
    rainfall_24h = np.clip(rainfall_24h, 0.0, 250.0)

    # 7-day rainfall correlates with 24h rainfall + antecedent precipitation
    rainfall_7d = rainfall_24h * np.random.uniform(1.8, 3.5, n_samples) + np.random.exponential(scale=40.0, size=n_samples)
    rainfall_7d = np.clip(rainfall_7d, rainfall_24h, 550.0)

    rainfall_intensity = rainfall_24h / np.random.uniform(4.0, 16.0, n_samples)
    rainfall_intensity = np.clip(rainfall_intensity, 0.0, 45.0)

    temperature = np.random.normal(loc=22.0, scale=6.0, size=n_samples)
    temperature = np.clip(temperature, 5.0, 40.0)

    humidity = 40.0 + (rainfall_24h * 0.22) + np.random.normal(loc=15.0, scale=8.0, size=n_samples)
    humidity = np.clip(humidity, 30.0, 99.0)

    # Terrain / DEM variables
    elevation = np.random.uniform(150.0, 3200.0, n_samples)
    slope = np.random.gamma(shape=3.5, scale=7.0, size=n_samples)  # Peak around 20-35 degrees
    slope = np.clip(slope, 2.0, 65.0)

    aspect = np.random.uniform(0.0, 360.0, n_samples)
    terrain_roughness = 0.2 + (slope / 70.0) * 0.6 + np.random.normal(0, 0.08, n_samples)
    terrain_roughness = np.clip(terrain_roughness, 0.05, 0.98)

    curvature = np.random.normal(loc=0.0, scale=0.45, size=n_samples)
    curvature = np.clip(curvature, -1.5, 1.5)

    # Remote Sensing / Satellite variables
    ndvi = np.random.beta(a=4.0, b=3.0, size=n_samples)
    ndvi = np.clip(ndvi, 0.05, 0.85)

    ndwi = np.random.uniform(-0.4, 0.5, n_samples)
    
    # Soil moisture correlates with rainfall, humidity, and NDWI
    soil_moisture = (
        0.20 +
        (rainfall_7d / 600.0) * 0.45 +
        (humidity / 100.0) * 0.20 +
        np.random.normal(0, 0.06, n_samples)
    )
    soil_moisture = np.clip(soil_moisture, 0.10, 0.98)

    vegetation_index = np.clip(ndvi + np.random.normal(0, 0.04, n_samples), 0.05, 0.90)

    # Historical variables
    historical_landslides = np.random.poisson(lam=1.2, size=n_samples)
    historical_landslides = np.clip(historical_landslides, 0, 10)
    previous_landslide = (historical_landslides > 0).astype(int)

    # Synthetic Ground Truth Probability formulation (Physical Hazard Index)
    # Higher risk factors:
    # 1. Slope > 28 deg
    # 2. Cumulative and 24h Rainfall
    # 3. High Soil Moisture
    # 4. Low NDVI (deforested/exposed soil)
    # 5. Prior Landslide history
    z = (
        -4.2
        + (slope / 30.0) * 2.4
        + (rainfall_24h / 75.0) * 2.1
        + (rainfall_7d / 200.0) * 1.6
        + (soil_moisture * 2.2)
        + (terrain_roughness * 1.5)
        - (ndvi * 1.8)
        + (historical_landslides * 0.45)
        + (previous_landslide * 0.70)
        + np.random.normal(0, 0.65, n_samples)
    )

    # Sigmoid function
    prob = 1.0 / (1.0 + np.exp(-z))
    landslide = (prob >= 0.50).astype(int)

    df = pd.DataFrame({
        "latitude": np.round(latitude, 4),
        "longitude": np.round(longitude, 4),
        "rainfall_24h": np.round(rainfall_24h, 2),
        "rainfall_7d": np.round(rainfall_7d, 2),
        "rainfall_intensity": np.round(rainfall_intensity, 2),
        "temperature": np.round(temperature, 2),
        "humidity": np.round(humidity, 2),
        "elevation": np.round(elevation, 1),
        "slope": np.round(slope, 2),
        "aspect": np.round(aspect, 1),
        "terrain_roughness": np.round(terrain_roughness, 3),
        "curvature": np.round(curvature, 3),
        "ndvi": np.round(ndvi, 3),
        "ndwi": np.round(ndwi, 3),
        "soil_moisture": np.round(soil_moisture, 3),
        "vegetation_index": np.round(vegetation_index, 3),
        "historical_landslides": historical_landslides,
        "previous_landslide": previous_landslide,
        "landslide": landslide
    })

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

    return df


def generate_single_demo_record(hazard_level: str = "random") -> Dict[str, Any]:
    """
    Generates a single realistic demo record according to requested hazard profile:
    'low', 'moderate', 'high', 'critical', or 'random'.
    """
    if hazard_level == "random":
        hazard_level = np.random.choice(["low", "moderate", "high", "critical"], p=[0.3, 0.3, 0.25, 0.15])

    if hazard_level == "low":
        return {
            "latitude": round(float(np.random.uniform(12.0, 20.0)), 4),
            "longitude": round(float(np.random.uniform(75.0, 82.0)), 4),
            "region_name": "Gentle Valley / Low Hazard Zone",
            "rainfall_24h": round(float(np.random.uniform(2.0, 20.0)), 1),
            "rainfall_7d": round(float(np.random.uniform(15.0, 65.0)), 1),
            "rainfall_intensity": round(float(np.random.uniform(1.0, 5.0)), 1),
            "temperature": round(float(np.random.uniform(22.0, 30.0)), 1),
            "humidity": round(float(np.random.uniform(45.0, 65.0)), 1),
            "wind_speed": round(float(np.random.uniform(5.0, 15.0)), 1),
            "elevation": round(float(np.random.uniform(200.0, 650.0)), 1),
            "slope": round(float(np.random.uniform(6.0, 16.0)), 1),
            "aspect": round(float(np.random.uniform(40.0, 280.0)), 1),
            "terrain_roughness": round(float(np.random.uniform(0.12, 0.35)), 2),
            "curvature": round(float(np.random.uniform(-0.15, 0.15)), 2),
            "ndvi": round(float(np.random.uniform(0.55, 0.78)), 2),
            "ndwi": round(float(np.random.uniform(-0.25, -0.05)), 2),
            "soil_moisture": round(float(np.random.uniform(0.20, 0.42)), 2),
            "vegetation_index": round(float(np.random.uniform(0.58, 0.80)), 2),
            "historical_landslides": 0,
            "previous_landslide": 0,
        }
    elif hazard_level == "moderate":
        return {
            "latitude": round(float(np.random.uniform(18.0, 26.0)), 4),
            "longitude": round(float(np.random.uniform(74.0, 85.0)), 4),
            "region_name": "Rolling Foothills / Moderate Monitoring Zone",
            "rainfall_24h": round(float(np.random.uniform(40.0, 75.0)), 1),
            "rainfall_7d": round(float(np.random.uniform(110.0, 190.0)), 1),
            "rainfall_intensity": round(float(np.random.uniform(7.0, 14.0)), 1),
            "temperature": round(float(np.random.uniform(19.0, 26.0)), 1),
            "humidity": round(float(np.random.uniform(68.0, 82.0)), 1),
            "wind_speed": round(float(np.random.uniform(10.0, 22.0)), 1),
            "elevation": round(float(np.random.uniform(750.0, 1350.0)), 1),
            "slope": round(float(np.random.uniform(20.0, 29.0)), 1),
            "aspect": round(float(np.random.uniform(60.0, 240.0)), 1),
            "terrain_roughness": round(float(np.random.uniform(0.40, 0.58)), 2),
            "curvature": round(float(np.random.uniform(-0.35, 0.35)), 2),
            "ndvi": round(float(np.random.uniform(0.40, 0.58)), 2),
            "ndwi": round(float(np.random.uniform(-0.10, 0.15)), 2),
            "soil_moisture": round(float(np.random.uniform(0.48, 0.65)), 2),
            "vegetation_index": round(float(np.random.uniform(0.42, 0.60)), 2),
            "historical_landslides": int(np.random.choice([0, 1, 2], p=[0.6, 0.3, 0.1])),
            "previous_landslide": 0,
        }
    elif hazard_level == "high":
        return {
            "latitude": round(float(np.random.uniform(25.0, 32.0)), 4),
            "longitude": round(float(np.random.uniform(85.0, 94.0)), 4),
            "region_name": "Steep Escarpment / High Alert Sector",
            "rainfall_24h": round(float(np.random.uniform(85.0, 135.0)), 1),
            "rainfall_7d": round(float(np.random.uniform(230.0, 340.0)), 1),
            "rainfall_intensity": round(float(np.random.uniform(15.0, 25.0)), 1),
            "temperature": round(float(np.random.uniform(16.0, 24.0)), 1),
            "humidity": round(float(np.random.uniform(82.0, 92.0)), 1),
            "wind_speed": round(float(np.random.uniform(18.0, 35.0)), 1),
            "elevation": round(float(np.random.uniform(1400.0, 2200.0)), 1),
            "slope": round(float(np.random.uniform(32.0, 42.0)), 1),
            "aspect": round(float(np.random.uniform(110.0, 260.0)), 1),
            "terrain_roughness": round(float(np.random.uniform(0.60, 0.78)), 2),
            "curvature": round(float(np.random.uniform(-0.70, 0.70)), 2),
            "ndvi": round(float(np.random.uniform(0.28, 0.42)), 2),
            "ndwi": round(float(np.random.uniform(0.12, 0.32)), 2),
            "soil_moisture": round(float(np.random.uniform(0.68, 0.82)), 2),
            "vegetation_index": round(float(np.random.uniform(0.29, 0.45)), 2),
            "historical_landslides": int(np.random.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1])),
            "previous_landslide": 1,
        }
    else:  # critical
        return {
            "latitude": round(float(np.random.uniform(27.0, 34.0)), 4),
            "longitude": round(float(np.random.uniform(88.0, 96.0)), 4),
            "region_name": "Alpine Ridge / Critical Debris Hazard Area",
            "rainfall_24h": round(float(np.random.uniform(140.0, 220.0)), 1),
            "rainfall_7d": round(float(np.random.uniform(350.0, 520.0)), 1),
            "rainfall_intensity": round(float(np.random.uniform(25.0, 42.0)), 1),
            "temperature": round(float(np.random.uniform(14.0, 21.0)), 1),
            "humidity": round(float(np.random.uniform(90.0, 98.0)), 1),
            "wind_speed": round(float(np.random.uniform(25.0, 48.0)), 1),
            "elevation": round(float(np.random.uniform(1800.0, 2900.0)), 1),
            "slope": round(float(np.random.uniform(38.0, 55.0)), 1),
            "aspect": round(float(np.random.uniform(140.0, 220.0)), 1),
            "terrain_roughness": round(float(np.random.uniform(0.75, 0.94)), 2),
            "curvature": round(float(np.random.uniform(0.40, 1.20)), 2),
            "ndvi": round(float(np.random.uniform(0.12, 0.28)), 2),
            "ndwi": round(float(np.random.uniform(0.28, 0.48)), 2),
            "soil_moisture": round(float(np.random.uniform(0.82, 0.96)), 2),
            "vegetation_index": round(float(np.random.uniform(0.15, 0.30)), 2),
            "historical_landslides": int(np.random.choice([3, 4, 5, 6])),
            "previous_landslide": 1,
        }
