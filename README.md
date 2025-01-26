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

### Linux/MacOS

```bash
curl -sSL https://install.python-poetry.org | python3 -
poetry install
poetry run uvicorn calendar_service.main:app --reload
```

### Windows

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
poetry install
poetry run uvicorn calendar_service.main:app --reload
```

## Environment Variables

- `DB_PATH`: SQLite database path (default: /data/calendar.db)
