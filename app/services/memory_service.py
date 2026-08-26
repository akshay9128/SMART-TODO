from sqlalchemy.orm import Session
from datetime import datetime
from app.models.memory import UserMemory
from app.models.user import User

def create_memory(
        memory_type :str,
        key:str,
        value:str,
        db:Session,
        current_user:User
)-> UserMemory:
    memory=UserMemory(
        user_id=current_user.id,
        memory_type=memory_type,
        key=key,
        value=value
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory

def get_memories(
        db:Session,
        current_user:User
)->list[UserMemory]:
    return(
        db.query(UserMemory)
        .filter(
            UserMemory.user_id==current_user.id
        )
        .order_by(UserMemory.id.desc())
        .all()
    )

def get_memory(
        memory_id:int,
        db:Session,
        current_user:User
)->UserMemory|None:

    return(
        db.query(UserMemory)
        .filter(
            UserMemory.id==memory_id,
            UserMemory.user_id==current_user.id
        )
        .first()
    )

def update_memory(
        memory_id:int,
        memory_type:str,
        key:str,
        value:str,
        db:Session,
        current_user:User
)->UserMemory|None:
    memory=get_memory(
        memory_id=memory_id,
        db=db,
        current_user=current_user
    )

    if memory is None:
        return None

    memory.memory_type=memory_type
    memory.key=key
    memory.value=value

    db.commit()
    db.refresh(memory)

    return memory

def delete_memory(
        memory_id:int,
        db:Session,
        current_user:User
)->bool:

    memory=get_memory(
        memory_id=memory_id,
        db=db,
        current_user=current_user
    )

    if memory is None:
        return False

    db.delete(memory)
    db.commit()

    return True

def save_preferred_reminder_time(
        reminder_time:str,
        db:Session,
        current_user:User
):
    existing_memory=(
        db.query(UserMemory)
        .filter(
            UserMemory.user_id==current_user.id,
            UserMemory.memory_type=="preference",
            UserMemory.key=="preferred_reminder_time"
        )
        .first()
    )

    if existing_memory:
        existing_memory.value=reminder_time
        existing_memory.updated_at=datetime.now()

        db.commit()
        db.refresh(existing_memory)

        return existing_memory

    memory=UserMemory(
        user_id=current_user.id,
        memory_type="preference",
        key="preferred_reminder_time",
        value=reminder_time
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory

def get_memory_by_key(
        key:str,
        db:Session,
        current_user:User
)-> UserMemory|None:
    return(
        db.query(UserMemory)
        .filter(
            UserMemory.user_id==current_user.id,
            UserMemory.key==key
        )
        .first()
    )

def get_user_memory(
    key: str,
    db: Session,
    current_user: User
):
    return get_memory_by_key(
        key=key,
        db=db,
        current_user=current_user
    )