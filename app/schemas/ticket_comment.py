from datetime import datetime

from pydantic import BaseModel


class TicketCommentCreate(BaseModel):
    comment: str


class TicketCommentResponse(BaseModel):
    id: int
    comment: str
    ticket_id: int
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }