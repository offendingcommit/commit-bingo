# Use slim Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables for Python and prevent the creation of .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS dependencies required for building some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Set working directory
WORKDIR /app

# Copy project metadata files and install dependencies (if using Poetry)
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry to not create a virtual environment and install dependencies
RUN poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-ansi --no-dev

# Copy the rest of the project
COPY . /app

# Expose port 8080 (if required)
EXPOSE 8080

# Set the default command to run the application
CMD ["python", "main.py"]