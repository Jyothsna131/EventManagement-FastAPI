from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from databaseSchemas.events import Base

class Attendee(Base):
    __tablename__="attendees"
    attendee_id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String,nullable=False)
    last_name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    phone_number=Column(String,nullable=False)
    event_id=Column(Integer,ForeignKey("events.event_id"))
    check_in_status=Column(Boolean,default=False)

