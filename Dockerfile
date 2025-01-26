FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --only main --no-root

COPY calendar_service/ ./calendar_service/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

ENV DB_PATH=/data/calendar.db

RUN mkdir /data

CMD ["poetry", "run", "uvicorn", "calendar_service.main:app", "--host", "0.0.0.0", "--port", "8000"]