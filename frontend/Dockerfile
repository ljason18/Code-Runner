# syntax=docker/dockerfile:1.4

ARG PYTHON_VERSION=3.12.7
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Run the application.
CMD ["python", "-m", "http.server", "8080"]
