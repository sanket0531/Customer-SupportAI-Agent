from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.repositories.ticket_repository import TicketRepository

from app.models.ticket_comment import TicketComment
from app.repositories.ticket_comment_repository import TicketCommentRepository
from app.schemas.ticket_comment import TicketCommentCreate


class TicketCommentService:

    @staticmethod
    def create_comment(
        db: Session,
        ticket_id: int,
        comment_data: TicketCommentCreate,
        current_user: User
    ):
        # 1. Get ticket
        ticket = TicketRepository.get_ticket_by_id(
            db=db,
            ticket_id=ticket_id
        )

        # 2. Ticket exists?
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found."
            )

        # 3. Authorization checks  ← ADD THEM HERE

        # Customer
        if (
            current_user.role == UserRole.CUSTOMER
            and ticket.customer_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to comment on this ticket."
            )

        # Agent
        if (
            current_user.role == UserRole.AGENT
            and ticket.assigned_agent_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to comment on this ticket."
            )

        # 4. Create ORM object
        comment = TicketComment(
            comment=comment_data.comment,
            ticket_id=ticket.id,
            user_id=current_user.id
        )

        # 5. Save using repository
        return TicketCommentRepository.create_comment(
            db=db,
            comment=comment
        )

    