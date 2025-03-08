# Use slim Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables for Python and prevent the creation of .pyc files
ARG BUILD_ENVIRONMENT

ENV BUILD_ENVIRONMENT=${BUILD_ENVIRONMENT} \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_CACHE_DIR=/root/.cache/pip \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.3

# Install OS dependencies required for building some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip && curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy project metadata files and install dependencies (if using Poetry)
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry to not create a virtual environment and install dependencies
RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
  --mount=type=cache,target=$PIP_CACHE_DIR \
  poetry install $(test "$BUILD_ENVIRONMENT" == production && echo "--only=main")

# Copy the rest of the project
COPY . /app

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port 8080 (if required)
EXPOSE 8080

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Set the default command to run the application
CMD ["poetry", "run", "python", "app.py"]