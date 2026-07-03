from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.ticket import TicketPriority, TicketStatus



class TicketCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    priority: TicketPriority = TicketPriority.MEDIUM


class TicketUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=5, max_length=200)
    description: Optional[str] = Field(default=None, min_length=10)
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_agent_id: Optional[int] = None


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    customer_id: int
    assigned_agent_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class AssignTicketRequest(BaseModel):
    assigned_to_id: int    