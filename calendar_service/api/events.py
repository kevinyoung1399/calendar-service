"""
API Routes Module
---------------
FastAPI router defining HTTP endpoints for event operations.
"""
import os
from typing import List, Optional
from calendar_service.db.repositories import SQLiteEventRepository
from calendar_service.models.event import EventCreate, EventResponse
from calendar_service.services.event_service import EventService
from fastapi import APIRouter, Depends

router = APIRouter()

def get_service():
    db_path = os.getenv('DB_PATH', 'calendar.db')
    repository = SQLiteEventRepository(db_path)
    return EventService(repository)

@router.post("/events", response_model=EventResponse)
async def create_event(event: EventCreate, service: EventService = Depends(get_service)):
    """
    Creates new calendar event.
    
    Request body:
        - description: Event description
        - time: Event time (YYYY-MM-DDTHH:MM:SS)
    """
    event = service.create_event(event.description, event.time)
    return {"id": event.id, "description": event.description, "time": event.time}

@router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, service: EventService = Depends(get_service)):
    """Retrieves event by ID."""
    event = service.get_event(event_id)
    return {"id": event.id, "description": event.description, "time": event.time}

@router.get("/events", response_model=List[EventResponse])
async def list_events(from_time: Optional[str] = None, to_time: Optional[str] = None, service: EventService = Depends(get_service)):
    """
    Lists events within time range.
    
    Query parameters:
        - from_time: Start time (default: start of current day)
        - to_time: End time (default: current time)
    """
    events = service.list_events(from_time, to_time)
    return [{"id": e.id, "description": e.description, "time": e.time} for e in events]