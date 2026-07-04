from sqlalchemy.orm import Session

from app.api.v1 import tickets
from app.models.ticket import Ticket
from app.schemas.ticket_filter import TicketFilter

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
    def _build_ticket_query(
        db: Session,
        filters: TicketFilter
    ):
        query = db.query(Ticket)

        if filters.status is not None:
            query = query.filter(
                Ticket.status == filters.status
            )

        if filters.priority is not None:
            query = query.filter(
                Ticket.priority == filters.priority
            )

        if filters.assigned_agent_id is not None:
            query = query.filter(
                Ticket.assigned_agent_id == filters.assigned_agent_id
            )

        return query    

    @staticmethod
    def get_all_tickets(
        db: Session,
        skip: int,
        limit: int,
        filters: TicketFilter
    ):
        query = TicketRepository._build_ticket_query(
            db=db,
            filters=filters
        )

        # Apply filters dynamically
        if filters.status is not None:
            query = query.filter(Ticket.status == filters.status)

        if filters.priority is not None:
            query = query.filter(Ticket.priority == filters.priority)

        if filters.assigned_agent_id is not None:
            query = query.filter(
                Ticket.assigned_agent_id == filters.assigned_agent_id
            )

        total = query.count()

        tickets = (
            query
            .order_by(Ticket.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return tickets, total
    
    @staticmethod
    def get_agent_tickets(
        db: Session,
        agent_id: int,
        skip: int,
        limit: int,
        filters: TicketFilter
    ):
        query = TicketRepository._build_ticket_query(
            db=db,
            filters=filters
        )

        query = query.filter(
            Ticket.assigned_agent_id == agent_id
        )

        total = query.count()

        tickets = (
            query
            .order_by(Ticket.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return tickets, total
    
    @staticmethod
    def get_customer_tickets(
        db: Session,
        customer_id: int,
        skip: int,
        limit: int,
        filters: TicketFilter
    ):
        query = TicketRepository._build_ticket_query(
            db=db,
            filters=filters
        )

        query = query.filter(
            Ticket.customer_id == customer_id
        )

        total = query.count()

        tickets = (
            query
            .order_by(Ticket.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return tickets, total

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