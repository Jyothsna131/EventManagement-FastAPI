from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from util.enums import EventStatus


class EventDTO(BaseModel):
    event_id: Optional[int] = None
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int
    status: EventStatus
