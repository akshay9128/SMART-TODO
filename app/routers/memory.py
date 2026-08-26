from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse,
    PreferredReminderTime
)
from app.services.memory_service import (
    create_memory,
    get_memories,
    get_memory,
    update_memory,
    delete_memory,
    save_preferred_reminder_time
)
from app.utils.time_parser import parse_reminder_time

router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)


@router.post("/", response_model=MemoryResponse)
def create_user_memory(
    request: MemoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_memory(
        memory_type=request.memory_type,
        key=request.key,
        value=request.value,
        db=db,
        current_user=current_user
    )


@router.get("/", response_model=list[MemoryResponse])
def list_user_memories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_memories(
        db=db,
        current_user=current_user
    )

@router.post("/preferred-reminder-time",response_model=MemoryResponse)
def set_preferred_reminder_time(
    request:PreferredReminderTime,
    db:Session=Depends(get_db),
    current_users:User=Depends(get_current_user)
):
    try:
        reminder_time=parse_reminder_time(request.time)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    return save_preferred_reminder_time(
        reminder_time=reminder_time,
        db=db,
        current_user=current_users
    )


@router.get("/{memory_id}", response_model=MemoryResponse)
def get_user_memory(
    memory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    memory = get_memory(
        memory_id=memory_id,
        db=db,
        current_user=current_user
    )

    if memory is None:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )

    return memory


@router.put("/{memory_id}", response_model=MemoryResponse)
def update_user_memory(
    memory_id: int,
    request: MemoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    memory = update_memory(
        memory_id=memory_id,
        memory_type=request.memory_type,
        key=request.key,
        value=request.value,
        db=db,
        current_user=current_user
    )

    if memory is None:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )

    return memory


@router.delete("/{memory_id}")
def delete_user_memory(
    memory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = delete_memory(
        memory_id=memory_id,
        db=db,
        current_user=current_user
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Memory not found"
        )

    return {
        "success": True,
        "message": "Memory deleted successfully"
    }


