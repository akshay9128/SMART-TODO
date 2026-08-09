from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.task import TaskCreate,TaskUpdate,TaskResponse
from app.models.task import Task



router=APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/",response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session=Depends(get_db)
    ):
    db_task=Task(
        title=task.title,
        category=task.category,
        priority=task.priority
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@router.get("/",response_model=list[TaskResponse])
def get_tasks(
    category:str |None=None,
    priority:str |None=None,
    completed:bool |None=None,
    db:Session =Depends(get_db)
):
    query=db.query(Task)

    if category is not None:
        query=query.filter(Task.category==category)

    if priority is not None:
        query=query.filter(Task.priority==priority)

    if completed is not None:
        query=query.filter(Task.completed==completed)
    return query.all()

@router.get("/{task_id}",response_model=TaskResponse)
def get_task(
    task_id:int,
    db:Session=Depends(get_db)
):
    task=db.query(Task).filter(Task.id==task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id:int,
    db:Session=Depends(get_db)
):
    task=db.query(Task).filter(Task.id==task_id).first()

    if task is None:
        return {"Message":"Task Not Found"}
    db.delete(task)
    db.commit()

    return {"Message":"Task Deleted Successfully"}

@router.put("/{task_id}",response_model=TaskResponse)
def update_task(
    task_id:int,
    task_data:TaskUpdate,
    db:Session=Depends(get_db)
):
    task=db.query(Task).filter(Task.id==task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )

    if task_data.title is not None:
        task.title=task_data.title

    if task_data.completed is not None:
        task.completed=task_data.completed

    if task_data.category is not None:
        task.category=task_data.category

    if task_data.priority is not None:
        task.priority=task_data.priority

    db.commit()
    db.refresh(task)

    return task

