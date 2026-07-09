from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.ticket_comment import (
    TicketCommentCreate,
    TicketCommentResponse
)
from app.services.ticket_comment_service import TicketCommentService

router = APIRouter(
    prefix="/tickets",
    tags=["Ticket Comments"]
)

@router.post(
    "/{ticket_id}/comments",
    response_model=TicketCommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    ticket_id: int,
    comment_data: TicketCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketCommentService.create_comment(
        db=db,
        ticket_id=ticket_id,
        comment_data=comment_data,
        current_user=current_user
    )