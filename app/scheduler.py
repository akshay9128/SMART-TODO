from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from app.database.session import SessionLocal
from app.models.task import Task
from app.services.reminder_services import send_reminder
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
            send_reminder(task,db)
            task.reminded=True
        db.commit()
    finally:
        db.close()
scheduler.add_job(check_due_tasks,"interval",seconds=10)
