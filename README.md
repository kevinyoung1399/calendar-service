# Calendar Service

A FastAPI-based Calendar API service.

## Quick Start (Users)

### Linux/MacOS

```bash
mkdir data
docker build -t calendar-service .
docker run -p 8000:8000 -v $(pwd)/data:/data calendar-service
```

### Windows

```powershell
mkdir data
docker build -t calendar-service .
docker run -p 8000:8000 -v ${PWD}/data:/data calendar-service
```

The API will be available at http://localhost:8000/docs

## Development Setup

Prerequisites:

- Python 3.10+
- Poetry

```
python -m poetry install
python -m poetry run uvicorn calendar_service.main:app --reload
```

## Environment Variables

- `DB_PATH`: SQLite database path (default: /data/calendar.db)

## Testing
```
python -m poetry run pytest
```

