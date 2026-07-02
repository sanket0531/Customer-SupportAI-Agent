from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate


class TicketRepository:

    @staticmethod
    def create_ticket(
        db: Session,
        ticket: Ticket
    ):
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def get_ticket_by_id(
        db: Session,
        ticket_id: int
    ):
        return (
            db.query(Ticket)
            .filter(Ticket.id == ticket_id)
            .first()
        )

    @staticmethod
    def get_all_tickets(
        db: Session
    ):
        return db.query(Ticket).all()

    @staticmethod
    def delete_ticket(
        db: Session,
        ticket: Ticket
    ):
        db.delete(ticket)
        db.commit()