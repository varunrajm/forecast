from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.database import init_database


configure_logging()
settings = get_settings()
init_database(settings.database_path)

app = FastAPI(
    title="Forecasta API",
    description="Sales and demand forecasting API with cleaning, modeling, metrics, and business insights.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.api_prefix)
