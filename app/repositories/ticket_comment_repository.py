from sqlalchemy.orm import Session

from app.models.ticket_comment import TicketComment


class TicketCommentRepository:

    @staticmethod
    def create_comment(
        db: Session,
        comment: TicketComment
    ):
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def get_comments_by_ticket(
        db: Session,
        ticket_id: int
    ):
        return (
            db.query(TicketComment)
            .filter(TicketComment.ticket_id == ticket_id)
            .order_by(TicketComment.created_at.asc())
            .all()
        )