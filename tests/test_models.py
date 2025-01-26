from calendar_service.models.event import Event

def test_event_creation():
    event = Event(id=1, description="Test Event", time="2025-01-01T10:00:00")
    assert event.id == 1
    assert event.description == "Test Event"
    assert event.time == "2025-01-01T10:00:00"

def test_event_from_row():
    row = (1, "Test Event", "2025-01-01T10:00:00")
    event = Event.from_row(row)
    assert event.id == 1
    assert event.description == "Test Event"
    assert event.time == "2025-01-01T10:00:00"