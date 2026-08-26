from app.database.base import Base
from app.database.connection import engine

from app.models.task import Task
from app.models.memory import UserMemory

def create_database():
    Base.metadata.create_all(bind=engine)