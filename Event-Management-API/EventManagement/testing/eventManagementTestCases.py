from http import client

import pytest
from unittest.mock import Mock

from _pytest import unittest
from sqlalchemy.orm import Session
from databaseSchemas.events import Event
from databaseSchemas.attendees import Attendee
from util.enums import EventType

# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)  # add assertion here

@pytest.fixture
def db_session():
    return Mock(spec=Session)

def test_create_event():
    event_data = {
        "name": "Test Tech Summit",
        "description": "A summit for discussing emerging technologies.",
        "start_time": "2025-03-15T09:00:00",
        "end_time": "2025-03-15T17:00:00",
        "location": "New York",
        "max_attendees": 100,
        "status": "scheduled"
    }
    response = client.post("/events/", json=event_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tech Summit"
    assert response.json()["status"] == "scheduled"

def test_add_attendee():
    attendee_data = {
        "first_name": "test",
        "last_name": "attendee",
        "email": "johndoe@example.com",
        "phone_number": "9876543210",
        "event_id": 10
    }
    response = client.post("/attendees/", json=attendee_data)
    assert response.status_code == 200
    assert response.json()["email"] == "johndoe@example.com"

def test_registration_limit(db_session):
    test_event = Event(
        name=" Test Tech Summit",
        description="Technology conference",
        start_time="2025-01-23 09:00",
        end_time="2025-01-25 18:00",
        location="Hyderabad",
        max_attendees=2,
        statu= EventType.scheduled
    )

    post_response = client.post("/events/", json=test_event)
    assert post_response.status_code == 201
    inserted_event = post_response.json()
    event_id = inserted_event["event_id"]

    # Simulate registered attendees
    test_attendees = [
        Attendee(first_name="test", last_name="Attendee1", email="attendee1@example.com",
                 phone_number="1234567990",event_id=event_id),
        Attendee(first_name="test", last_name="Attendee2", email="attendee2@example.com",
                 phone_number="1234567990",event_id=event_id)
    ]

    for attendee in test_attendees:
        post_response = client.post("/attendees/", json=test_event)
        assert post_response.status_code == 201
        inserted_attendee = post_response.json()

    # Act: Attempt to add a third attendee
    new_attendee = Attendee(first_name="Another", last_name="Attendee", email="another@example.com",
                            phone_number="1234567990",event_id=event_id)
    post_response = client.post("/attendees/", json=test_event)
    assert post_response.status_code == 400

if __name__ == '__main__':
    unittest.main()
