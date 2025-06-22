.PHONY: help install test lint format clean run build docker-build docker-run

# Help command
help:
	@echo "BINGO Application Makefile Commands"
	@echo ""
	@echo "Basic Commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run the application"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean build artifacts and cache"
	@echo ""
	@echo "Test Commands (Progressive):"
	@echo "  make test-unit    - Run unit tests only (fastest)"
	@echo "  make test-quick   - Run unit + fast integration tests"
	@echo "  make test         - Run all tests with coverage"
	@echo "  make test-e2e     - Run end-to-end browser tests (slowest)"
	@echo ""
	@echo "Specialized Test Commands:"
	@echo "  make test-smoke   - Run critical smoke tests"
	@echo "  make test-state   - Run StateManager tests"
	@echo "  make test-ui      - Run UI component tests"
	@echo "  make test-watch   - Run unit tests in watch mode"
	@echo "  make test-failed  - Re-run only failed tests"
	@echo ""
	@echo "Build Commands:"
	@echo "  make build        - Build the package"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

# Install dependencies
install:
	poetry install

# Run application
run:
	poetry run python main.py

# Run modular app (when available)
run-modular:
	poetry run python app.py

# Run all tests
test:
	poetry run pytest --cov=src

# Test categories - Progressive from fastest to slowest
test-unit:
	@echo "Running unit tests (fast, isolated)..."
	poetry run pytest -m unit -v

test-integration:
	@echo "Running integration tests..."
	poetry run pytest -m integration -v

test-e2e:
	@echo "Running end-to-end tests (requires app running on :8080)..."
	poetry run pytest -m e2e -v

# Quick test combinations
test-quick:
	@echo "Running quick tests (unit + fast integration)..."
	poetry run pytest -m "unit or (integration and not slow)" -v

test-smoke:
	@echo "Running smoke tests (critical functionality)..."
	poetry run pytest -m smoke -v

# Component-specific tests
test-state:
	@echo "Running StateManager tests..."
	poetry run pytest -m state -v

test-ui:
	@echo "Running UI component tests..."
	poetry run pytest -m ui -v

test-persistence:
	@echo "Running persistence tests..."
	poetry run pytest -m persistence -v

# Special test modes
test-watch:
	@echo "Running tests in watch mode..."
	poetry run ptw --runner "pytest -m unit -x" tests/

test-parallel:
	@echo "Running tests in parallel..."
	poetry run pytest -n auto -v

test-failed:
	@echo "Re-running failed tests..."
	poetry run pytest --lf -v

# Performance and coverage
test-coverage:
	poetry run pytest --cov=src --cov-report=term-missing --cov-report=html

test-benchmark:
	@echo "Test Suite Performance Report:"
	@echo "============================="
	@time -p poetry run pytest -m unit --tb=no -q
	@echo ""
	@time -p poetry run pytest -m integration --tb=no -q
	@echo ""
	@time -p poetry run pytest -m e2e --tb=no -q

# Run lints
lint:
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
	poetry run black --check .
	poetry run isort --check .

# Format code
format:
	poetry run black .
	poetry run isort .

# Clean build artifacts and cache
clean:
	rm -rf dist
	rm -rf .pytest_cache
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Build package
build:
	poetry build

# Docker commands
docker-build:
	docker build -t bingo .

docker-run:
	docker run -p 8080:8080 bingo