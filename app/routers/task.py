from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.task import TaskCreate
from app.models.task import Task


router=APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session=Depends(get_db)
    ):
    db_task=Task(
        title=task.title
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task
