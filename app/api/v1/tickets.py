from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    AssignTicketRequest
)
from app.schemas.ticket_schema import AssignTicketRequest
from app.services.ticket_service import TicketService

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post(
    "/",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketService.create_ticket(
        db=db,
        ticket_data=ticket_data,
        current_user=current_user
    )


@router.get(
    "/",
    response_model=list[TicketResponse]
)
def get_all_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketService.get_all_tickets(db)


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketService.get_ticket_by_id(
        db,
        ticket_id
    )


@router.put(
    "/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketService.update_ticket(
        db,
        ticket_id,
        ticket_data
    )

@router.put(
    "/{ticket_id}/assign",
    response_model=TicketResponse
)
def assign_ticket(
    ticket_id: int,
    assign_data: AssignTicketRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketService.assign_ticket(
        db=db,
        ticket_id=ticket_id,
        assign_data=assign_data,
        current_user=current_user
    )


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TicketService.delete_ticket(
        db,
        ticket_id
    )