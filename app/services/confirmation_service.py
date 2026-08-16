from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User


def confirm_delete_task(
    task_id: int,
    db: Session,
    current_user: User
) -> dict:

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
        .first()
    )

    if task is None:
        return {
            "success": False,
            "action": "delete_task",
            "task_id": task_id,
            "message": "Task not found"
        }

    db.delete(task)
    db.commit()

    return {
        "success": True,
        "action": "delete_task",
        "task_id": task_id,
        "message": "Task deleted successfully"
    }