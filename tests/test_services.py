import pytest
from fastapi import HTTPException
from calendar_service.services.event_service import EventService

def test_create_event_success(service):
    event = service.create_event("Test Event", "2025-01-01T10:00:00")
    assert event.description == "Test Event"
    assert event.time == "2025-01-01T10:00:00"

def test_create_event_invalid_datetime(service):
    with pytest.raises(HTTPException) as exc:
        service.create_event("Test Event", "invalid-datetime")
    assert exc.value.status_code == 400

def test_get_event_success(service):
    created = service.create_event("Test Event", "2025-01-01T10:00:00")
    retrieved = service.get_event(created.id)
    assert retrieved.id == created.id
    assert retrieved.description == created.description

def test_get_event_not_found(service):
    with pytest.raises(HTTPException) as exc:
        service.get_event(999)
    assert exc.value.status_code == 404

def test_list_events_success(service):
    service.create_event("Event 1", "2025-01-01T10:00:00")
    service.create_event("Event 2", "2025-01-02T10:00:00")
    
    events = service.list_events(
        "2025-01-01T00:00:00",
        "2025-01-02T23:59:59"
    )
    assert len(events) == 2