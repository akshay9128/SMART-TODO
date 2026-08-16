from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.agent import AgentRequest
from app.services.agent_service import process_task_request


router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)


@router.post("/")
def process_agent_request(
    request: AgentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    return process_task_request(
        text=request.text,
        db=db,
        current_user=current_user,
        confirmed=request.confirmed
    )