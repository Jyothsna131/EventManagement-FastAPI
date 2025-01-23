from http import client

import pytest
from unittest.mock import Mock

from _pytest import unittest
from sqlalchemy.orm import Session
from databaseSchemas.events import Event
from databaseSchemas.attendees import Attendee
from util.enums import EventStatus
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

def test_add_attendee():
    test_event = {
        "name": "Test Tech add attendee",
        "description": "A summit for testing.",
        "start_time": "2025-03-15T09:00:00",
        "end_time": "2025-03-25T17:00:00",
        "location": "New York",
        "max_attendees": 2,
        "status": "scheduled"
    }

    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech add attendee"
    assert response.json()["status"] == "scheduled"
    event_id = response.json()["event_id"]
    attendee_data = {
        "first_name": "test",
        "last_name": "attendee",
        "email": "test_add_attendee@example.com",
        "phone_number": "9876543210",
        "event_id": event_id
    }
    response = client.post("/attendees/", json=attendee_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test_add_attendee@example.com"

def test_registration_limit():
    test_event = {
       "name": "Test Tech Summit Max Limit 4",
        "description": "A summit for testing.",
        "start_time": "2025-03-15T09:00:00",
        "end_time": "2025-03-25T17:00:00",
        "location": "New York",
        "max_attendees": 2,
        "status": "scheduled"
            }

    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Summit Max Limit 4"
    assert response.json()["status"] == "scheduled"
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

def test_checkin_tooearly():
    test_event = {
           "name": "Test Tech CheckIn",
            "description": "A summit for CheckIn testing.",
            "start_time": "2025-03-24T09:00:00",
            "end_time": "2025-03-25T17:00:00",
            "location": "New York",
            "max_attendees": 2,
            "status": "scheduled"
                }
    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech CheckIn"
    assert response.json()["status"] == "scheduled"
    event_id = response.json()["event_id"]

    attendee={"first_name":"Attendee", "last_name":"CheckIn", "email":"attendee_checkin@example.com",
                 "phone_number":"1234567990","event_id":event_id}
    post_attendee = client.post("/attendees/", json=attendee)
    assert post_attendee.status_code==200
    attendee_id=post_attendee.json()["attendee_id"]
    check_in_url = f"/attendees/check_in/{attendee_id}"
    response = client.put(check_in_url)
    assert response.status_code == 403

def test_checkin_valid():
    test_event = {
           "name": "Test Tech CheckIn Valid",
            "description": "A summit for CheckIn Valid testing.",
            "start_time": "2025-01-22T09:00:00",
            "end_time": "2025-01-28T17:00:00",
            "location": "New York",
            "max_attendees": 2,
            "status": "scheduled"
                }
    response = client.post("/events/", json=test_event)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech CheckIn Valid"
    assert response.json()["status"] == "scheduled"
    event_id = response.json()["event_id"]

    attendee={"first_name":"Attendee", "last_name":"CheckIn", "email":"attendee_checkin_valid@example.com",
                 "phone_number":"1234567990","event_id":event_id}
    post_attendee = client.post("/attendees/", json=attendee)
    assert post_attendee.status_code==200
    attendee_id=post_attendee.json()["attendee_id"]
    check_in_url = f"/attendees/check_in/{attendee_id}"
    response = client.put(check_in_url)
    assert response.status_code == 200

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

if __name__ == '__main__':
    unittest.main()

