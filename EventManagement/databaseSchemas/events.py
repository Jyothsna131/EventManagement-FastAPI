from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import declarative_base
from util.enums import EventStatus

Base = declarative_base()

class Event(Base):
    __tablename__="events"
    event_id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    description=Column(String,nullable=True)
    start_time=Column(DateTime,nullable=False)
    end_time=Column(DateTime,nullable=False)
    location=Column(String,nullable=False)
    max_attendees=Column(Integer,nullable=False)
    status=Column(Enum(EventStatus), default='scheduled')