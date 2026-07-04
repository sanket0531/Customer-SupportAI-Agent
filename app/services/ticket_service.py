from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import ticket
from app.models.ticket import Ticket, TicketStatus
from app.models.user import User, UserRole
from app.repositories.ticket_repository import TicketRepository
from app.schemas.pagination import PaginatedResponse
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate, AssignTicketRequest

from app.repositories.user_repository import UserRepository
from app.schemas.ticket_filter import TicketFilter

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
    def _validate_ticket_access(
        ticket: Ticket,
        current_user: User
    ) -> None:
        """
        Validates whether the current user has permission
        to access the specified ticket.
        """
        
        # Admins can access everything.
        if current_user.role == UserRole.ADMIN:
            return

        # Agents can only access tickets assigned to them.
        if current_user.role == UserRole.AGENT:
            if ticket.assigned_agent_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not assigned to this ticket."
                )
            return

        # Customers can only access their own tickets.
        if current_user.role == UserRole.CUSTOMER:
            if ticket.customer_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to access this ticket."
                )
            return

    @staticmethod
    def get_ticket_by_id(
        db: Session,
        ticket_id: int,
        current_user: User
    ):
        ticket = TicketRepository.get_ticket_by_id(db, ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )

        TicketService._validate_ticket_access(
            ticket=ticket,
            current_user=current_user
        )

        return ticket
    
    @staticmethod
    def get_all_tickets(
        db: Session,
        current_user: User,
        page: int,
        size: int,
        filters: TicketFilter
    ):
        skip = (page - 1) * size

        print("========== DEBUG ==========")
        print("User ID:", current_user.id)
        print("User Role:", current_user.role)
        print("Role Type:", type(current_user.role))
        print("===========================")

        if current_user.role == UserRole.ADMIN:
            tickets, total = TicketRepository.get_all_tickets(
                db=db,
                skip=skip,
                limit=size,
                filters=filters
            )

        elif current_user.role == UserRole.AGENT:
            tickets, total = TicketRepository.get_agent_tickets(
                db=db,
                agent_id=current_user.id,
                skip=skip,
                limit=size,
                filters=filters
            )

        else:
            tickets, total = TicketRepository.get_customer_tickets(
                db=db,
                customer_id=current_user.id,
                skip=skip,
                limit=size,
                filters=filters
            )

        return PaginatedResponse[TicketResponse].create(
            items=tickets,
            total=total,
            page=page,
            size=size,
        )
    
    @staticmethod
    def update_ticket(
        db: Session,
        ticket_id: int,
        ticket_data: TicketUpdate,
        current_user: User
    ):
        ticket = TicketRepository.get_ticket_by_id(db, ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )
        TicketService._validate_ticket_access(
            ticket=ticket,
            current_user=current_user
        )    


        update_data = ticket_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(ticket, key, value)

        return TicketRepository.save(
            db=db,
            ticket=ticket
        )
    
    @staticmethod
    def delete_ticket(
        db: Session,
        ticket_id: int,
        current_user: User
    ):
        ticket = TicketRepository.get_ticket_by_id(db, ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )
        
        TicketService._validate_ticket_access(
            ticket=ticket,
            current_user=current_user
        )

        TicketRepository.delete_ticket(db, ticket)

        return {
            "message": "Ticket deleted successfully"
        }
    
    @staticmethod
    def assign_ticket(
        db: Session,
        ticket_id: int,
        assign_data: AssignTicketRequest,
        current_user: User
    ):
        # Only ADMIN can assign tickets
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can assign tickets."
            )

        # Get ticket
        ticket = TicketRepository.get_ticket_by_id(db, ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found."
            )

        # Get agent
        agent = UserRepository.get_user_by_id(
            db,
            assign_data.assigned_agent_id
        )

        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found."
            )

        # Verify role
        if agent.role != UserRole.AGENT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user must have AGENT role."
            )

        # Assign ticket
        ticket.assigned_agent_id = agent.id
        ticket.status = TicketStatus.IN_PROGRESS

        return TicketRepository.save(db, ticket)