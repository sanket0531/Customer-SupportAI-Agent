from app.database.base import Base

from app.models.user import User
from app.models.ticket import Ticket
from app.models.ticket_comment import TicketComment

print(Base.metadata.tables.keys())