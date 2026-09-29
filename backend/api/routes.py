from fastapi import APIRouter
from datetime import datetime
from backend.config import settings

router = APIRouter()


@router.get("/")
def get_root():
    return {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "demo_mode": True,
        "disclaimer": "DEMO / SIMULATED DATA — Pure AI Prototype without IoT physical sensors",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/health")
def get_health():
    models_ready = settings.XGB_MODEL_PATH.exists() and settings.SCALER_PATH.exists()
    return {
        "status": "healthy",
        "models_loaded": models_ready,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
