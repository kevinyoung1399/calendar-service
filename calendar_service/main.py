"""
Calendar Service FastAPI Application
-----------------------------------
A REST API service for managing calendar events. Uses FastAPI framework
with SQLite backend storage.

Usage:
    python main.py

Environment Variables:
    DB_PATH: SQLite database file path (default: calendar.db)
"""
from fastapi import FastAPI
from calendar_service.api import events

app = FastAPI()
app.include_router(events.router)

@app.get("/health", status_code=200)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "calendar-service"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)