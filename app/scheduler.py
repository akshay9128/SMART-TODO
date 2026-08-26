from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime,timedelta

from app.database.session import SessionLocal
from app.models.task import Task
from app.services.reminder_services import send_reminder
scheduler=BackgroundScheduler()


def create_next_occurrence(task, db):
    if not task.recurrence_type:
        return None

    if not task.due_at:
        return None

    if task.recurrence_type == "daily":
        next_due = task.due_at + timedelta(days=1)

    elif task.recurrence_type == "weekly":
        next_due = task.due_at + timedelta(days=7)

    else:
        return None

    next_reminder = None

    if task.reminder_at is not None:
        reminder_offset = task.due_at - task.reminder_at
        next_reminder = next_due - reminder_offset

    next_task = Task(
        user_id=task.user_id,
        title=task.title,
        category=task.category,
        priority=task.priority,
        due_at=next_due,
        reminder_at=next_reminder,
        recurrence_type=task.recurrence_type,
        recurrence_value=task.recurrence_value,
        completed=False,
        reminded=False,
    )

    db.add(next_task)
    return next_task


        
def check_due_tasks():
    db=SessionLocal()
    try:
        now=datetime.now()
        tasks=(
            db.query(Task)
            .filter(
                Task.reminder_at<= now,
                Task.completed==False,
                Task.reminded==False
            )
            .all()
        )
        for task in tasks:
            send_reminder(task,db)
            task.reminded=True
            if task.recurrence_type:
                create_next_occurrence(task,db)
        db.commit()
    finally:
        db.close()
scheduler.add_job(check_due_tasks,"interval",seconds=10)
