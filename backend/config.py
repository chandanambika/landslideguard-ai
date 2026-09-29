import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "AI-Based Early Warning & Landslide Risk Monitoring System"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEMO_MODE: bool = True
    
    # Paths
    DATASET_PATH: Path = DATA_DIR / "landslide_dataset.csv"
    XGB_MODEL_PATH: Path = MODELS_DIR / "xgboost_landslide_model.pkl"
    RF_MODEL_PATH: Path = MODELS_DIR / "rf_landslide_model.pkl"
    SCALER_PATH: Path = MODELS_DIR / "scaler.pkl"
    METRICS_PATH: Path = MODELS_DIR / "model_metrics.json"
    DATABASE_PATH: Path = BASE_DIR / "landslide.db"

    # Optional external keys (demo runs offline if not present)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    GOOGLE_EARTH_ENGINE_PROJECT: str = os.getenv("GOOGLE_EARTH_ENGINE_PROJECT", "")

    # Risk Thresholds
    RISK_THRESHOLD_LOW: float = 25.0
    RISK_THRESHOLD_MODERATE: float = 50.0
    RISK_THRESHOLD_HIGH: float = 75.0


settings = Settings()
