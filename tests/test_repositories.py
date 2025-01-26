import pytest
from datetime import datetime
from calendar_service.models.event import Event

def test_create_event(repository):
    event = Event(id=None, description="Event 1", time="2025-01-01T10:00:00")
    created = repository.create(event)
    assert created.id is not None
    assert created.description == "Event 1"
    assert created.time == "2025-01-01T10:00:00"

def test_get_event_by_id(repository):
    event = Event(id=None, description="Event 1", time="2025-01-01T10:00:00")
    created = repository.create(event)
    retrieved = repository.get_by_id(created.id)
    assert retrieved.id == created.id
    assert retrieved.description == created.description
    assert retrieved.time == created.time

def test_get_event_by_timerange(repository):
    # Create test events
    repository.create(Event(id=None, description="Event 1", time="2025-01-01T10:00:00"))
    repository.create(Event(id=None, description="Event 2", time="2025-01-02T10:00:00"))
    repository.create(Event(id=None, description="Event 3", time="2026-01-03T10:00:00"))

    events = repository.get_by_timerange(
        "2025-01-01T00:00:00",
        "2025-01-02T23:59:59"
    )
    assert len(events) == 2
    assert events[0].description == "Event 1"
    assert events[1].description == "Event 2"