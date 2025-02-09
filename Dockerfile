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
RUN poetry install $(test "$BUILD_ENVIRONMENT" == production && echo "--only=main")

# Copy the rest of the project
COPY . /app

# Expose port 8080 (if required)
EXPOSE 8080

# Set the default command to run the application
CMD ["python", "main.py"]