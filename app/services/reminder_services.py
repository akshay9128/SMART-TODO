from app.models.notification import Notification


def send_reminder(task, db):

    message = (
        f"Task '{task.title}' is due "
        f"(ID: {task.id}, Priority: {task.priority})"
    )

    print(
        "\n🔔 Task REMINDER:"
        "\n----------------------------------"
        f"\nTask: {task.title}"
        f"\nID: {task.id}"
        f"\nPriority: {task.priority}"
        f"\nDUE: {task.due_at}"
        "\n----------------------------------"
    )

    notification = Notification(
        task_id=task.id,
        message=message,
        is_read=False
    )

    db.add(notification)