"""
FastAPI Application Entrypoint
AI-Based Early Warning & Landslide Risk Monitoring System (Pure AI, No IoT)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.config import settings
from backend.database import init_db
from backend.api.routes import router as general_router
from backend.api.prediction_routes import router as prediction_router
from backend.api.data_routes import router as data_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("landslide_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure database, dataset, and model artifacts exist
    logger.info("Initializing LandslideGuard AI backend...")
    init_db()

    # Verify if model is trained; if missing, train automatically
    if not settings.XGB_MODEL_PATH.exists() or not settings.SCALER_PATH.exists():
        logger.info("Trained model or scaler not found. Training models on startup...")
        from backend.ml.train_model import train_and_evaluate_all
        train_and_evaluate_all()
    else:
        logger.info("Trained models and scalers detected.")

    yield
    logger.info("Shutting down LandslideGuard AI backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Academic/Demo prototype for pure AI landslide risk monitoring and early warning without IoT hardware.",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits Vite dev server, local origins, and production preview
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(general_router)
app.include_router(prediction_router)
app.include_router(data_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
