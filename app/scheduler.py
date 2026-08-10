from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from app.database.session import SessionLocal
from app.models.task import Task
scheduler=BackgroundScheduler()

def check_due_tasks():
    db=SessionLocal()
    try:
        now=datetime.now()
        tasks=(
            db.query(Task)
            .filter(
                Task.due_at<= now,
                Task.completed==False,
                Task.reminded==False
            )
            .all()
        )
        for task in tasks:
            print(
                f"Due task:{task.title}"
                f"(id={task.id},priority={task.priority})"
            )
            task.reminded=True
        db.commit()
    finally:
        db.close()
scheduler.add_job(check_due_tasks,"interval",seconds=10)
