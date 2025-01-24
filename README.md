# Event Management API
### Overview
The Event Management API provides functionalities for managing events and attendees, including the creation of events, registration of attndees,
status updates for events, and attendee check-ins. The project is buit using FastAPI, SQLAlchemy, and Pydantic.
The system is designed to handle event scheduling, attendee registration, event updates, and bulk operations like check-ins.

### Features
#### 1. Event Management
- Crete, read, update, and delete events
- Automatically update event status based on the event's end time
- Search events by status, location, and date
#### 2. Attendee Management
- Register attendees for events, with a limit on the number of attendees
- Update attendee details
- Check-in functionality, including validation to prevent early check-is or check-ins after an event ends
- Bulk check-in of attendees via CSV upload
#### 3. Event Status:
- Event status can be scheduled, ongoing, completed, or canceled
- Status updates automatically based on event start and end times

### Technologies Used
  - **Backend Framework:** FastAPI
  - **Database:** MySQL
  - **ORM:** SQLAlchemy
  - **Data Validation:** Pydantic
  - **Testing:** Pytest

 ### Project Structure
 <pre>
EventManagementProject/
   |
   |-controller/
     |-eventManagementController.py
     |-attendeesController.py
   |-databaseSchemas/
     |-events.py
     |-attendees.py
   |-model/
     |-eventDTO.py
     |-attendeesDTO.py
   |-config/
     |-dbConfiguration.py
   |-util/
     |-enums.py
   |-main.py
   |-testCases.py
   |-requirements.txt
 </pre>

### Installation
#### 1. Clone the Repository
```
git clone https:github.com/Jyothsna131/event-management-api.git
cd event-management-api
```
#### 2. Install Dependencies
```
pip install -r requirements.txt
```
#### 3. Database Configuration
Update the database connection URL in config/dbConfiguration.py to match your local or production MySQL instance:
```
db_url="mysql+pymysql://root:password@localhost:port/event_management"
```
#### 4. Create Database Tables
Ensure that the database exists (create database event_management in your MySQL) and run the following command to create necessary tables:
```
python
from databaseSchemas.events import Base,engine
Base.metadata.create_all(bind=engine)
```
#### 5. Run the API
Start the FastAPI app:
```
uvicorn main:app --reload
```
The API will be accessible at http://127.0.0.1:8000

#### 6. Access the Documentation
FastAPI provides automatic Swagger UI documentation for our API:
- Open browser and visit: http://127.0.0.1:8000/docs

### API Endpoints
#### Event Endpoints
- **POST** /events/: Create a new event
- **GET** /events/{event_id}: Get an event by ID
- **GET** /events/: Get a list of events (with optional filter like status, location, and date)
- **PUT** /events/{event_id}: Update an event
- **DELETE** /events/{event_id}: Delete an event

#### Attendee Endpoints
- **POST** /attendees/: Add a new attendee to an event
- **GET** /attendees/: Get a list of attendees for an event
- **GET** /attendees/all: Get all attendees across events
- **PUT** /attendees/{attendee_id}: Update an attendee
- **DELETE** /attendees/{attendee_id}: Delete an attendee
- **PUT** /attendees/check_in/{attendee_id}: Check in an attendee
- **POST** /attendees/bulk-check-in: Bulk check-in attendees via CSV

### Testing
Run unit tests to ensure everygthing works as expected:
```
pytest testCases.py
```



    
