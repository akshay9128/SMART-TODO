from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger
from app.database.create_db import create_database
from app.routers.task import router as task_router
from app.scheduler import scheduler
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()
    
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)



create_database()
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
