def test_create_event_api(client):
    response = client.post("/events", json={
        "description": "Test Event",
        "time": "2025-01-01T10:00:00"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test Event"
    assert data["time"] == "2025-01-01T10:00:00"

def test_get_event_api(client):
    # Create event first
    create_response = client.post("/events", json={
        "description": "Test Event",
        "time": "2025-01-01T10:00:00"
    })
    event_id = create_response.json()["id"]

    # Get event
    response = client.get(f"/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_id
    assert data["description"] == "Test Event"

def test_list_events_api(client):
    # Create test events
    client.post("/events", json={
        "description": "Event 1",
        "time": "2025-01-01T10:00:00"
    })
    client.post("/events", json={
        "description": "Event 2", 
        "time": "2025-01-02T10:00:00"
    })

    response = client.get("/events", params={
        "from_time": "2025-01-01T00:00:00",
        "to_time": "2025-01-02T23:59:59"
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2