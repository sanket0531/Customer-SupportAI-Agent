from pydantic import BaseModel

class AssignTicketRequest(BaseModel):
    assigned_agent_id: int

class UpdateTicketRequest(BaseModel):
    title: str
    description: str
    status: str

class TicketUpdate(BaseModel):
    title: str
    description: str
    status: str
    