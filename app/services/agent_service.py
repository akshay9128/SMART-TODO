from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.agents.task_agent import TaskAgent
from app.utils.date_parser import parse_due_date


agent = TaskAgent()


def process_task_request(
    text: str,
    db: Session,
    current_user: User,
    confirmed: bool = False
) -> dict:

    result = agent.process(text)

    # ============================================================
    # CREATE TASK
    # ============================================================

    if result["intent"] == "create_task":

        due_at = parse_due_date(
            result["due_date"],
            result["due_time"]
        )

        task = Task(
            user_id=current_user.id,
            title=result["task_title"],
            category=result["category"],
            priority=result["priority"],
            due_at=due_at,
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        # Build natural response
        message = f'🎉 Done! I created the task "{task.title}"'

        if task.due_at:
            message += f' for {task.due_at.strftime("%B %d at %I:%M %p").lstrip("0")}'

        message += "."

        return {
            "success": True,
            "action": "create_task",
            "task_id": task.id,
            "message": message
        }


    # ============================================================
    # DELETE TASK
    # ============================================================

    elif result["intent"] == "delete_task":

        if result["task_id"] is None:
            return {
                "success": False,
                "action": "delete_task",
                "message": "I need the task ID to delete it."
            }

        task = (
            db.query(Task)
            .filter(
                Task.id == result["task_id"],
                Task.user_id == current_user.id
            )
            .first()
        )

        if task is None:
            return {
                "success": False,
                "action": "delete_task",
                "task_id": result["task_id"],
                "message": f"I couldn't find task {result['task_id']}."
            }

        # Confirmation required
        if not confirmed:
            return {
                "success": False,
                "action": "delete_task",
                "task_id": result["task_id"],
                "requires_confirmation": True,
                "message": (
                    f'⚠️ Are you sure you want to delete '
                    f'task {task.id} "{task.title}"?'
                )
            }

        # Delete after confirmation
        task_id = task.id
        task_title = task.title

        db.delete(task)
        db.commit()

        return {
            "success": True,
            "action": "delete_task",
            "task_id": task_id,
            "message": (
                f'🗑️ Done! I deleted task {task_id} '
                f'"{task_title}".'
            )
        }


    # ============================================================
    # COMPLETE TASK
    # ============================================================

    elif result["intent"] == "complete_task":

        if result["task_id"] is None:
            return {
                "success": False,
                "action": "complete_task",
                "message": "I need the task ID to complete it."
            }

        task = (
            db.query(Task)
            .filter(
                Task.id == result["task_id"],
                Task.user_id == current_user.id
            )
            .first()
        )

        if task is None:
            return {
                "success": False,
                "action": "complete_task",
                "task_id": result["task_id"],
                "message": f"I couldn't find task {result['task_id']}."
            }

        task.completed = True
        db.commit()

        return {
            "success": True,
            "action": "complete_task",
            "task_id": task.id,
            "message": (
                f'✅ Done! "{task.title}" has been marked as completed.'
            )
        }


    # ============================================================
    # LIST TASKS
    # ============================================================

    elif result["intent"] == "list_tasks":

        print("\n========== AGENT USER DEBUG ==========")
        print("CURRENT USER ID:", current_user.id)
        print("CURRENT USERNAME:", current_user.username)
        print("=====================================")

        tasks = (
        db.query(Task)
        .filter(Task.user_id == current_user.id)
        .order_by(Task.id.desc())
        .all()
    )
        
        

        task_lines = []

        for index, task in enumerate(tasks, start=1):

            status = "DONE" if task.completed else "TODO"

            line = (
            f"{index:>2}. {status:<4}  "
            f"{task.title}"
        )

            if task.priority:
                line += f" | Priority: {task.priority}"

            if task.category:
                line += f" | Category: {task.category}"

            if task.due_at:
                due = task.due_at.strftime(
                "%B %d at %I:%M %p"
            ).lstrip("0")

                line += f" | Due: {due}"

            task_lines.append(line)

        message = (
        f"📋 You have {len(tasks)} tasks:\n\n"
        + "\n".join(task_lines)
    )

        return {
        "success": True,
        "action": "list_tasks",
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "priority": task.priority,
                "category": task.category,
                "due_at": task.due_at.isoformat()
                if task.due_at else None,
            }
            for task in tasks
        ],
        "message": message,
    }


    # ============================================================
    # UPDATE TASK
    # ============================================================

    elif result["intent"] == "update_task":

        if result["task_id"] is None:
            return {
                "success": False,
                "action": "update_task",
                "message": "I need the task ID to update it."
            }

        task = (
            db.query(Task)
            .filter(
                Task.id == result["task_id"],
                Task.user_id == current_user.id
            )
            .first()
        )

        if task is None:
            return {
                "success": False,
                "action": "update_task",
                "task_id": result["task_id"],
                "message": f"I couldn't find task {result['task_id']}."
            }

        changes = []

        if result["task_title"]:
            task.title = result["task_title"]
            changes.append(f'title to "{task.title}"')

        if result["priority"]:
            task.priority = result["priority"]
            changes.append(f"priority to {task.priority}")

        if result["category"]:
            task.category = result["category"]
            changes.append(f"category to {task.category}")

        db.commit()
        db.refresh(task)

        if changes:
            message = (
                f'✏️ Done! I updated task {task.id}: '
                + ", ".join(changes)
                + "."
            )
        else:
            message = f"✏️ Task {task.id} was updated."

        return {
            "success": True,
            "action": "update_task",
            "task_id": task.id,
            "message": message
        }


    # ============================================================
    # UNKNOWN / NOT IMPLEMENTED
    # ============================================================

    return {
        "success": False,
        "action": result["intent"],
        "message": (
            "🤔 I'm not sure what you want me to do. "
            "You can ask me to create, update, complete, "
            "list, or delete a task."
        )
    }