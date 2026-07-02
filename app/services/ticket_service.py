from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ticket import Ticket, TicketStatus
from app.models.user import User
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketService:

    @staticmethod
    def create_ticket(
        db: Session,
        ticket_data: TicketCreate,
        current_user: User
    ):
        ticket = Ticket(
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            status=TicketStatus.OPEN,
            customer_id=current_user.id
        )

        return TicketRepository.create_ticket(db, ticket)

    @staticmethod
    def get_ticket_by_id(
        db: Session,
        ticket_id: int
    ):
        ticket = TicketRepository.get_ticket_by_id(db, ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )

        return ticket

    @staticmethod
    def get_all_tickets(
        db: Session
    ):
        return TicketRepository.get_all_tickets(db)

    @staticmethod
    def update_ticket(
        db: Session,
        ticket_id: int,
        ticket_data: TicketUpdate
    ):
        ticket = TicketRepository.get_ticket_by_id(db, ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )

        update_data = ticket_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(ticket, key, value)

        db.commit()
        db.refresh(ticket)

        return ticket

    @staticmethod
    def delete_ticket(
        db: Session,
        ticket_id: int
    ):
        ticket = TicketRepository.get_ticket_by_id(db, ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )

        TicketRepository.delete_ticket(db, ticket)

        return {
            "message": "Ticket deleted successfully"
        }