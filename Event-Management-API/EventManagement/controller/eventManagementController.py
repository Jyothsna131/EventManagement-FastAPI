from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from model.eventDTO import EventDTO
from model.attendeesDTO import AttendeesDTO
from databaseSchemas.events import Event
from databaseSchemas.attendees import Attendee
from config.dbConfiguration import get_db
from datetime import datetime, date
from util.enums import EventStatus


router = APIRouter(prefix="/events",tags=["Events"])
#db: Session = Depends(get_db)
@router.post("/", response_model=EventDTO)
def create_event(event: EventDTO, db: Session = Depends(get_db)):
    # Check if an event with the same name already exists
    db_event = db.query(Event).filter(Event.name == event.name).first()
    if db_event:
        raise HTTPException(status_code=400, detail="Event with this name already exists.")

    # Create a new event instance
    db_event = Event(
        name=event.name,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time,
        location=event.location,
        max_attendees=event.max_attendees,
        status=event.status
    )

    # Add event to session and commit
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event

# Get event by ID
@router.get("/{event_id}", response_model=EventDTO)
def get_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found.")

    curr_datetime=datetime.now()
    if db_event.end_time<curr_datetime and db_event.status!=EventStatus.completed:
        db_event.status=EventStatus.completed
        db.commit()
        db.refresh(db_event)
    return db_event

# Get all events
@router.get("/", response_model=list[EventDTO])
def get_all_events(status:str=None,location:str=None, date: date = None, db: Session = Depends(get_db)):
    query = db.query(Event)

    curr_datetime = datetime.now()
    events_to_update = query.filter(Event.end_time < curr_datetime, Event.status != EventStatus.completed).all()

    for event in events_to_update:
        event.status = EventStatus.completed

    db.commit()


    if status:
        query= query.filter(Event.status == status)
    if location:
        query.filter(Event.location == location)
    if date:
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())

        query = query.filter(and_(
            Event.start_time <= end_of_day,
            Event.end_time >= start_of_day
        ))

    events=query.all()

    if not events:
        raise HTTPException(status_code=404,detail="No events found with given search criterea")

    return events

# Update an event
@router.put("/{event_id}", response_model=EventDTO)
def update_event(event_id: int, event: EventDTO, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found.")

    # Update event details
    db_event.name = event.name
    db_event.description = event.description
    db_event.start_time = event.start_time
    db_event.end_time = event.end_time
    db_event.location = event.location
    db_event.max_attendees = event.max_attendees
    db_event.status = event.status

    db.commit()
    db.refresh(db_event)

    return db_event

# Delete an event
@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found.")

    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully."}





