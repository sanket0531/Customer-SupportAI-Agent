from typing import Optional

from pydantic import BaseModel

from app.models.ticket import TicketStatus, TicketPriority


class TicketFilter(BaseModel):
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_agent_id: Optional[int] = None