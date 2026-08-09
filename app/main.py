from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger
from app.database.create_db import create_databse
from app.routers.task import router as task_router
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

create_databse()
app.include_router(task_router)

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
