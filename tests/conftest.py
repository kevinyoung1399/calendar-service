import os
import pytest
from fastapi.testclient import TestClient
from calendar_service.db.repositories import SQLiteEventRepository
from calendar_service.services.event_service import EventService
from calendar_service.main import app
import sqlite3

@pytest.fixture(autouse=True)
def cleanup_db(test_db):
    yield
    os.remove(test_db)

@pytest.fixture
def test_db():
    """Creates test database and returns its path."""
    db_path = 'calendar_test.db'
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS events
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         description TEXT NOT NULL,
         time TEXT NOT NULL)
    ''')
    conn.close()
    return db_path

@pytest.fixture
def repository(test_db):
    return SQLiteEventRepository(test_db)

@pytest.fixture
def service(test_db):
    repo = SQLiteEventRepository(test_db)
    return EventService(repo)

@pytest.fixture
def client(test_db):
    """Creates TestClient with overridden dependencies for integration testing."""
    os.environ['DB_PATH'] = test_db
    repo = SQLiteEventRepository(test_db)
    service = EventService(repo)
    app.dependency_overrides[EventService] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()
    del os.environ['DB_PATH']