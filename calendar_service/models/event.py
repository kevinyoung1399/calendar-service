"""
Event Models Module
-----------------
Pydantic models for event data validation and serialization.
"""
from pydantic import BaseModel
from typing import Optional

class EventCreate(BaseModel):
    """Request model for event creation."""
    description: str
    time: str

class EventResponse(BaseModel):
    """Response model for event data."""
    id: int
    description: str
    time: str

class Event(BaseModel):
    """Internal event model with database mapping."""
    id: Optional[int] = None
    description: str
    time: str

    @classmethod
    def from_row(cls, row: tuple) -> 'Event':
        """Creates Event instance from database row."""
        return cls(id=row[0], description=row[1], time=row[2])

    class Config:
        """Enables ORM mode for database integration."""
        from_attributes = True 