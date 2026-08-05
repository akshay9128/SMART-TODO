from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)


@app.get("/")
def home():
    logger.info("Home endpoint called")

    return {
        "message": "Welcome to AI TODO Assistant",
        "version": settings.VERSION,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }