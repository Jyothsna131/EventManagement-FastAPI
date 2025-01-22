from fastapi import FastAPI
from controller.eventManagementController import router as event_router
from controller.attendeesController import attendee_router as attendee_router

app = FastAPI()
print("FastAPI app is starting...")
# Include the event router

app.include_router(event_router)
app.include_router(attendee_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Management API!"}