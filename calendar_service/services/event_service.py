"""
Event Service Module
------------------
Business logic layer for calendar event operations.
Handles event validation and repository interactions.
"""
from datetime import datetime
from fastapi import HTTPException
from typing import List, Optional

from calendar_service.db.repositories import EventRepository
from calendar_service.models.event import Event


class EventService:
    """
    Service class for handling calendar event operations.
    
    Attributes:
        repository (EventRepository): Data access layer for events
    """
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def create_event(self, description: str, time: str) -> Event:
        self._validate_datetime(time)
        """
        Creates a new calendar event.
        
        Args:
            description: Event description text
            time: Event time in ISO format (YYYY-MM-DDTHH:MM:SS)
            
        Returns:
            Event: Created event with assigned ID
            
        Raises:
            HTTPException: If datetime format is invalid
        """
        return self.repository.create(Event(id=None, description=description, time=time))

    def get_event(self, event_id: int) -> Event:
        """
        Retrieves event by ID.
        
        Args:
            event_id: Event identifier
            
        Returns:
            Event: Found event
            
        Raises:
            HTTPException: If event not found
        """
        event = self.repository.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    def list_events(self, from_time: Optional[str], to_time: Optional[str]) -> List[Event]:
        """
        Lists events within specified time range.
        
        Args:
            from_time: Start time in ISO format (default: start of current day)
            to_time: End time in ISO format (default: current time)
            
        Returns:
            List[Event]: Events within time range
            
        Raises:
            HTTPException: If datetime format is invalid
        """
        from_time = from_time or datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        ).strftime("%Y-%m-%dT%H:%M:%S")
        to_time = to_time or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        self._validate_datetime(from_time)
        self._validate_datetime(to_time)
        return self.repository.get_by_timerange(from_time, to_time)

    def _validate_datetime(self, time_str: str):
        """Validates ISO datetime format."""
        try:
            datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid datetime format")