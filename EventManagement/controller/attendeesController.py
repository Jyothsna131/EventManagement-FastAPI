from fastapi import APIRouter, HTTPException, Depends,UploadFile, File
from sqlalchemy import Boolean
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import truediv

from model.attendeesDTO import AttendeesDTO
from databaseSchemas.events import Event
from databaseSchemas.attendees import Attendee
from config.dbConfiguration import get_db
from datetime import datetime, timedelta

import csv
from io import StringIO

attendee_router = APIRouter(prefix="/attendees",tags=["Attendees"])

# Add attendee to an event
@attendee_router.post("/", response_model=AttendeesDTO)
def add_attendee(attendee: AttendeesDTO, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.event_id == attendee.event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found. Please try with another")

    # Check if the attendee already exists
    existing_attendee = db.query(Attendee).filter(Attendee.email == attendee.email).first()
    if existing_attendee:
        raise HTTPException(status_code=400, detail="Attendee with this email already exists.")

    # Check if the event is full
    attendee_count = db.query(Attendee).filter(Attendee.event_id == attendee.event_id).count()
    if attendee_count >= db_event.max_attendees:
        raise HTTPException(status_code=400, detail="Event is already full.")

    # Add attendee
    db_attendee = Attendee(
        first_name=attendee.first_name,
        last_name=attendee.last_name,
        email=attendee.email,
        phone_number=attendee.phone_number,
        event_id=attendee.event_id,
    )
    try:
        db.add(db_attendee)
        db.commit()
        db.refresh(db_attendee)
        return db_attendee
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error: " + str(e))

@attendee_router.get("/", response_model=list[AttendeesDTO])
def get_all_attendees(event_id:int,check_in_status:bool=None,db: Session = Depends(get_db)):
    event=db.query(Event).filter(Event.event_id==event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    query = db.query(Attendee).filter(Attendee.event_id==event_id)

    if check_in_status is not None:
        query=query.filter(Attendee.check_in_status==check_in_status)

    attendees=query.all()
    if not attendees:
        raise HTTPException(status_code=404,detail="No attendees found for search criterea")
    return attendees

@attendee_router.put("/{attendee_id}", response_model=AttendeesDTO)
def update_attendee(attendee_id: int , attendee: AttendeesDTO, db: Session = Depends(get_db)):
    db_attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
    if not db_attendee:
        raise HTTPException(status_code=404, detail="Attendee not found.")

    db_attendee.first_name = attendee.first_name
    db_attendee.last_name = attendee.last_name
    db_attendee.email = attendee.email
    db_attendee.phone_number = attendee.phone_number
    db_attendee.event_id = attendee.event_id

    db.commit()
    db.refresh(db_attendee)

    return db_attendee

@attendee_router.delete("/{attendee_id}")
def delete_attendee(attendee_id:int,db:Session=Depends(get_db)):
    db_attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
    if not db_attendee:
        raise HTTPException(status_code=404, detail="Attendee not found.")

    db.delete(db_attendee)
    db.commit()
    return {"message": "Attendee deleted successfully."}

@attendee_router.put("/check_in/{attendee_id}")
def checkIn_attendee(attendee_id:int, db:Session=Depends(get_db)):
    db_attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
    if not db_attendee:
        raise HTTPException(status_code=404, detail="You are not registered for any event")
    db_event = db.query(Event).filter(Event.event_id == db_attendee.event_id).first()

    current_time = datetime.now()

    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    if current_time < db_event.start_time - timedelta(hours=1):
        raise HTTPException(status_code=403, detail="Check-in is not allowed before 1 hour of event start time.")

    # Disallow check-in if the event has already ended
    if current_time > db_event.end_time:
        raise HTTPException(status_code=403, detail="Event has already ended. Check-in is not allowed.")

    db_attendee.check_in_status = True
    db.commit()
    db.refresh(db_attendee)
    return {"message": "You are successfuly checked-in"}

@attendee_router.post("/bulk-check-in", status_code=200)
async def bulk_check_in(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Please upload a valid CSV file.")

    content = await file.read()
    csv_data = StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csv_data)

    if reader.fieldnames:
        fieldnames = [header.strip() for header in reader.fieldnames]  # Remove whitespace or BOM
    else:
        fieldnames = None

    if "attendee_id" not in fieldnames or "event_id" not in fieldnames:
        raise HTTPException(status_code=400, detail={
                "error": "CSV must contain the required columns.",
                "provided_headers": fieldnames
            })

    errors = []
    for row in reader:
        attendee_id = row.get("attendee_id")
        event_id = row.get("event_id")

        if not attendee_id or not event_id:
            errors.append({"row": row, "error": "Missing 'attendee_id' or 'event_id'."})
            continue

        attendee = db.query(Attendee).filter(
            Attendee.attendee_id == int(attendee_id),
            Attendee.event_id == int(event_id)
        ).first()

        if attendee:
            attendee.checked_in = True
        else:
            errors.append({"row": row, "error": "Attendee not found."})

    db.commit()

    if errors:
        return {
            "message": "Bulk check-in completed with some errors.",
            "errors": errors
        }

    return {"message": "All attendees successfully checked in."}