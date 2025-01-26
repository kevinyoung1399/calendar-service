"""
Event Repository Module
---------------------
Data access layer for event persistence using SQLite.
"""
from abc import ABC, abstractmethod
import sqlite3
from typing import List, Optional
from calendar_service.models.event import Event
import contextlib

class EventRepository(ABC):
    """Abstract base class defining event storage operations."""
    
    @abstractmethod
    def create(self, event: Event) -> Event:
        """Creates new event."""
        pass

    @abstractmethod
    def get_by_id(self, event_id: int) -> Optional[Event]:
        """Retrieves event by ID."""
        pass

    @abstractmethod
    def get_by_timerange(self, from_time: str, to_time: str) -> List[Event]:
        """Lists events within time range."""
        pass


class SQLiteEventRepository(EventRepository):
    """SQLite implementation of event storage."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _init_db(self):
        """Creates events table if not exists."""
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS events
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                time TEXT NOT NULL)
            ''')

    @contextlib.contextmanager 
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def create(self, event: Event) -> Event:
        """
        Creates new event.
        
        Args:
            event: Event to create (without ID)
            
        Returns:
            Event: Created event with assigned ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO events (description, time) VALUES (?, ?)",
                (event.description, event.time)
            )
            conn.commit()
            event_id = cursor.lastrowid
            cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
            return Event.from_row(cursor.fetchone())

    def get_by_id(self, event_id: int) -> Optional[Event]:
        """
        Retrieves event by ID.
        
        Args:
            event_id: Event identifier
            
        Returns:
            Optional[Event]: Found event or None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
            row = cursor.fetchone()
            return Event.from_row(row) if row else None

    def get_by_timerange(self, from_time: str, to_time: str) -> List[Event]:
        """
        Lists events within time range.
        
        Args:
            from_time: Start of time range
            to_time: End of time range
            
        Returns:
            List[Event]: Events within the specified time range
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM events WHERE time BETWEEN ? AND ?",
                (from_time, to_time)
            )
            return [Event.from_row(row) for row in cursor.fetchall()]