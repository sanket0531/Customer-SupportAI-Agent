from sqlalchemy.orm import Session

from app.models.ticket import Ticket


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
    def update_ticket(
        db: Session,
        ticket: Ticket,
        updated_ticket
    ):
        ticket.title = updated_ticket.title
        ticket.description = updated_ticket.description
        ticket.status = updated_ticket.status
        ticket.assigned_to_id = updated_ticket.assigned_to_id

        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def save(
        db: Session,
        ticket: Ticket
    ):
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def delete_ticket(
        db: Session,
        ticket: Ticket
    ):
        db.delete(ticket)
        db.commit()