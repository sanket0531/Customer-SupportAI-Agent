from pydantic import BaseModel

class AssignTicketRequest(BaseModel):
    assigned_to_id: int

class UpdateTicketRequest(BaseModel):
    title: str
    description: str
    status: str