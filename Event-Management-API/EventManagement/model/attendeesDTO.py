from pydantic import BaseModel
from typing import Optional


class AttendeesDTO(BaseModel):
    attendee_id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    phone_number: str
    event_id: int
    check_in_status: Optional[bool] = False
