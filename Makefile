.PHONY: help install test lint format clean run run-monolithic build docker-build docker-run

# Help command
help:
	@echo "BINGO Application Makefile Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make install        - Install dependencies"
	@echo "  make run            - Run the modular application"
	@echo "  make run-monolithic - Run the original monolithic application"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linters"
	@echo "  make format         - Format code"
	@echo "  make clean          - Clean build artifacts and cache"
	@echo "  make build          - Build the package"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-run     - Run Docker container"

# Install dependencies
install:
	poetry install

# Run application (modular version)
run:
	poetry run python app.py

# Run original monolithic application
run-monolithic:
	poetry run python main.py

# Run tests
test:
	poetry run pytest --cov=src

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