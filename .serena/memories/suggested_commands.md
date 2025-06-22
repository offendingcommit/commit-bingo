# Bingo Project - Suggested Commands

## Development Commands

### Setup & Installation
```bash
# Quick setup
./setup.sh

# Manual setup
poetry install
```

### Running the Application
```bash
# Run modular application (preferred)
poetry run python app.py

# Run legacy monolithic version
poetry run python main.py

# Using Make
make run
make run-modular
```

### Testing
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test file
poetry run pytest tests/test_game_logic.py

# Run specific test
poetry run pytest -v tests/test_ui_functions.py::TestUIFunctions::test_header_updates_on_both_paths

# Using Make
make test
```

### Code Quality
```bash
# Run all linters
poetry run flake8 main.py src/ tests/
poetry run black --check .
poetry run isort --check .
poetry run mypy .

# Format code
poetry run black .
poetry run isort .

# Using Make
make lint
make format
```

### Docker Commands
```bash
# Build Docker image
docker build -t bingo .

# Run Docker container
docker run -p 8080:8080 bingo

# Using Make
make docker-build
make docker-run
```

### Kubernetes/Helm
```bash
# Deploy with Helm
cd helm && ./package.sh
helm install bingo ./bingo
```

### CI/CD Pipeline Check (Pre-Push)
```bash
# Full pre-push check sequence
poetry run flake8 main.py src/ tests/
poetry run black --check .
poetry run isort --check .
poetry run pytest
poetry run python main.py  # Ctrl+C after confirming it starts
```

### Cleanup
```bash
# Clean build artifacts
make clean
```

### Git Operations
```bash
# Feature branch
git checkout -b feature/description-of-change

# Commit with conventional format
git commit -m "feat(scope): add new feature"
git commit -m "fix(ui): resolve connection issue"
git commit -m "chore: update dependencies"
```

## Darwin/macOS Specific Commands
- Use `open .` to open current directory in Finder
- Use `pbcopy` and `pbpaste` for clipboard operations
- File paths are case-insensitive by default
- Use `ls -la` for detailed directory listings
- Use `find . -name "*.py"` for file searching