from http import client
import pytest
from fastapi.testclient import TestClient
from main import app

client=TestClient(app)


def test_create_event():
    event_data = {
        "name": "Test Tech Summit1",
        "description": "A summit for discussing emerging technologies.",
        "start_time": "2025-03-15T09:00:00",
        "end_time": "2025-03-15T17:00:00",
        "location": "New York",
        "max_attendees": 100,
        "status": "scheduled"
    }
    response = client.post("/events/", json=event_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Summit1"
    assert response.json()["status"] == "scheduled"

# Test get event by id
def test_get_event():
    event_data = {
        "name": "Test Tech Summit2",
        "description": "Second summit for discussing emerging technologies.",
        "start_time": "2025-01-15T09:00:00",
        "end_time": "2025-01-30T17:00:00",
        "location": "New York",
        "max_attendees": 100,
        "status": "scheduled"
    }
    response = client.post("/events/", json=event_data)
    assert response.status_code == 200
    event_id=response.json()["event_id"]
    response=client.get(f"/events/{event_id}")

#test get all events
def test_get_all_events():
    response=client.get("/events/")
    assert response.status_code==200

def test_update_event():
    old_event = {
        "name": "Test Old Tech Summit1",
        "description": "A summit for discussing emerging old technologies.",
        "start_time": "2025-01-15T09:00:00",
        "end_time": "2025-01-25T17:00:00",
        "location": "New York",
        "max_attendees": 100,
        "status": "scheduled"
    }
    response = client.post("/events/", json=old_event)
    assert response.status_code == 200
    assert response.json()["name"] =="Test Old Tech Summit1"
    assert response.json()["status"] == "scheduled"

    event_id = response.json()["event_id"]
    new_data = {
        "name": "Test New Tech Summit1",
        "description": "A summit for discussing emerging new technologies.",
        "start_time": "2025-01-15T09:00:00",
        "end_time": "2025-01-25T17:00:00",
        "location": "New York",
        "max_attendees": 20,
        "status": "scheduled"
    }
    url=f"/events/{event_id}"
    response=client.put(url,json=new_data)
    assert response.status_code==200
    assert response.json()["name"]=="Test New Tech Summit1"

def test_delete_event():
    event_data = {
        "name": "Test Tech Summit for Deletion",
        "description": "Second summit for discussing emerging technologies.",
        "start_time": "2025-02-15T09:00:00",
        "end_time": "2025-02-28T17:00:00",
        "location": "New York",
        "max_attendees": 100,
        "status": "scheduled"
    }
    response = client.post("/events/", json=event_data)
    assert response.status_code == 200
    event_id = response.json()["event_id"]
    response=client.delete(f"events/{event_id}")
    assert response.status_code==200
    assert response.json()=={"message":"Event deleted successfully."}

def test_add_attendee():
    test_event = {
        "name": "Test Tech Summit add attendee",
        "description": "A summit for testing add attendee.",
        "start_time": "2025-03-15T09:00:00",
        "end_time": "2025-03-25T17:00:00",
        "location": "New York",
        "max_attendees": 2,
        "status": "scheduled"
    }

    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Summit add attendee"

    event_id = response.json()["event_id"]
    attendee_data = {
        "first_name": "attendee1",
        "last_name": "testadd",
        "email": "test_add_attendee1@example.com",
        "phone_number": "9876543210",
        "event_id": event_id
    }
    response = client.post("/attendees/", json=attendee_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test_add_attendee1@example.com"

def test_get_attendee():
    test_event = {
        "name": "Test Tech Summit get attendee",
        "description": "A summit for testing get attendee.",
        "start_time": "2025-03-15T09:00:00",
        "end_time": "2025-03-25T17:00:00",
        "location": "New York",
        "max_attendees": 2,
        "status": "scheduled"
    }

    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Summit get attendee"

    event_id = response.json()["event_id"]
    attendee_data = {
        "first_name": "attendee1",
        "last_name": "testget",
        "email": "test_get_attendee1@example.com",
        "phone_number": "9876543210",
        "event_id": event_id
    }
    response = client.post("/attendees/", json=attendee_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test_get_attendee1@example.com"

    attendee_id=response.json()["attendee_id"]
    response=client.get(f"/attendees/{attendee_id}")
    assert response.status_code==200
    assert response.json()["attendee_id"]==attendee_id
    assert response.json()["email"]=="test_get_attendee1@example.com"

def test_get_attendeesofEvent():
    test_event = {
        "name": "Test Tech Summit get all attendees registered for particular Event",
        "description": "A summit for testing to get all attendees of particular Event",
        "start_time": "2025-04-15T09:00:00",
        "end_time": "2025-05-25T17:00:00",
        "location": "New York",
        "max_attendees": 20,
        "status": "scheduled"
    }

    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Summit get all attendees registered for particular Event"
    event_id = response.json()["event_id"]

    test_attendees = [
        {"first_name": "test", "last_name": "Attendee1", "email": "attendeeget1@example.com",
         "phone_number": "1234567990", "event_id": event_id},
        {"first_name": "test", "last_name": "Attendee2", "email": "attendeeget2@example.com",
         "phone_number": "1234567990", "event_id": event_id}
    ]

    for attendee in test_attendees:
        post_response = client.post("/attendees/", json=attendee)
        assert post_response.status_code == 200

    response=client.get(f"/attendees/ofevent/{event_id}")
    assert response.status_code==200

def test_update_attendee():
    test_event = {
        "name": "Test Tech Summit update attendee",
        "description": "A summit for testing update attendee.",
        "start_time": "2025-03-15T09:00:00",
        "end_time": "2025-03-25T17:00:00",
        "location": "New York",
        "max_attendees": 2,
        "status": "scheduled"
    }

    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Summit update attendee"

    event_id = response.json()["event_id"]
    attendee_data = {
        "first_name": "attendee1",
        "last_name": "testupdate",
        "email": "test_update_attendee1@example.com",
        "phone_number": "9876543210",
        "event_id": event_id
    }
    response = client.post("/attendees/", json=attendee_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test_update_attendee1@example.com"

    attendee_id = response.json()["attendee_id"]
    updated_attendee = {
        "first_name": "attendeeUpdated",
        "last_name": "test",
        "email": "test_updatedone_attendee1@example.com",
        "phone_number": "9876543210",
        "event_id": event_id
    }
    response=client.put(f"/attendees/{attendee_id}",json=updated_attendee)
    assert response.status_code==200
    assert response.json()["email"]=="test_updatedone_attendee1@example.com"

def test_delete_attendee():
    test_event = {
        "name": "Test Tech Summit delete attendee",
        "description": "A summit for testing delete attendee.",
        "start_time": "2025-01-15T09:00:00",
        "end_time": "2025-02-25T17:00:00",
        "location": "Hyderabad",
        "max_attendees": 2,
        "status": "scheduled"
    }

    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Summit delete attendee"

    event_id = response.json()["event_id"]
    attendee_data = {
        "first_name": "attendee1",
        "last_name": "testdelete",
        "email": "test_delete_attendee1@example.com",
        "phone_number": "9876543212",
        "event_id": event_id
    }
    response = client.post("/attendees/", json=attendee_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test_delete_attendee1@example.com"

    attendee_id = response.json()["attendee_id"]
    response=client.delete(f"attendees/{attendee_id}")
    assert response.status_code==200
    assert response.json()=={"message": "Attendee deleted successfully."}

    response=client.get(f"/attendees/{attendee_id}")
    assert response.status_code==404
    assert response.json()["detail"]=="Attendee not found."

def test_registration_limit():
    test_event = {
       "name": "Test Tech Summit Max Limit",
        "description": "A summit for testing registration limit.",
        "start_time": "2025-04-15T09:00:00",
        "end_time": "2025-05-25T17:00:00",
        "location": "New York",
        "max_attendees": 2,
        "status": "scheduled"
            }

    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Summit Max Limit"
    event_id = response.json()["event_id"]


    test_attendees = [
        {"first_name":"test", "last_name":"Attendee1", "email":"attendee1@example.com",
                 "phone_number":"1234567990","event_id":event_id},
        {"first_name": "test", "last_name": "Attendee2", "email": "attendee2@example.com",
         "phone_number": "1234567990", "event_id": event_id}
    ]

    for attendee in test_attendees:
        post_response = client.post("/attendees/", json=attendee)
        assert post_response.status_code == 200
        inserted_attendee = post_response.json()

    # Act: Attempt to add a third attendee
    new_attendee = {"first_name":"test", "last_name":"Attendee3", "email":"attendee3@example.com",
                 "phone_number":"1234567910","event_id":event_id}
    post_response = client.post("/attendees/", json=new_attendee)
    assert post_response.status_code == 400

def test_checkinInvalidAttendee():
    attendee_id=100
    check_in_url=f"/attendees/check_in/{attendee_id}"
    response=client.put(check_in_url)
    assert response.status_code==404
    assert response.json()["detail"]=="You are not registered for any event"

def test_checkin_tooearly():
    test_event = {
           "name": "Test Tech CheckIn too Early",
            "description": "A summit for too early CheckIn testing.",
            "start_time": "2025-03-24T09:00:00",
            "end_time": "2025-03-25T17:00:00",
            "location": "New York",
            "max_attendees": 2,
            "status": "scheduled"
                }

    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech CheckIn too Early"
    event_id = response.json()["event_id"]

    attendee={"first_name":"Attendee", "last_name":"CheckIn", "email":"attendee_checkin@example.com",
                 "phone_number":"1234567990","event_id":event_id}
    post_attendee = client.post("/attendees/", json=attendee)
    assert post_attendee.status_code==200
    attendee_id=post_attendee.json()["attendee_id"]

    check_in_url = f"/attendees/check_in/{attendee_id}"
    response = client.put(check_in_url)
    assert response.status_code == 403
    assert response.json()["detail"]=="Check-in is not allowed before 1 hour of event start time."

def test_valid_checkin():
    test_event = {
           "name": "Test Tech Valid CheckIn",
            "description": "A summit for Valid CheckIn testing.",
            "start_time": "2025-01-23T09:00:00",
            "end_time": "2025-01-31T17:00:00",
            "location": "New York",
            "max_attendees": 2,
            "status": "scheduled"
                }
    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Valid CheckIn"
    event_id = response.json()["event_id"]

    attendee={"first_name":"Attendee", "last_name":"CheckIn", "email":"attendee_checkin_valid@example.com",
                 "phone_number":"1234567990","event_id":event_id}
    post_attendee = client.post("/attendees/", json=attendee)
    assert post_attendee.status_code==200
    attendee_id=post_attendee.json()["attendee_id"]
    check_in_url = f"/attendees/check_in/{attendee_id}"
    response = client.put(check_in_url)
    assert response.status_code == 200
    assert response.json()=={"message":"You are successfuly checked-in"}

def test_automatic_satus_updates():
    test_event = {
        "name": "Test Tech Automatic Status Update",
        "description": "A summit for status update.",
        "start_time": "2025-01-12T09:00:00",
        "end_time": "2025-01-20T17:00:00",
        "location": "New York",
        "max_attendees": 2,
        "status": "scheduled"
    }
    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Automatic Status Update"
    assert response.json()["status"] == "completed"



if __name__ == '__main__':
    unittest.main()

