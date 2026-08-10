from app.database.base import Base
from app.database.connection import engine

from app.models.task import Task

def create_database():
    Base.metadata.create_all(bind=engine)