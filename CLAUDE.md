# BINGO Project Guide

## Build Commands
```bash
# Install dependencies
poetry install

# Run application
poetry run python main.py

# Build Docker container
docker build -t bingo .

# Run Docker container
docker run -p 8080:8080 bingo

# Helm deployment
cd helm && ./package.sh && helm install bingo ./bingo
```

## Code Style Guidelines
- **Imports**: Standard library first, third-party second, local modules last
- **Formatting**: Use f-strings for string formatting
- **Constants**: Defined at top of file in UPPER_CASE
- **Naming**: snake_case for functions/variables, UPPER_CASE for constants
- **Error Handling**: Use try/except blocks with proper logging
- **UI Elements**: Define class constants for styling
- **Logging**: Use Python's logging module with descriptive messages
- **Comments**: Use docstrings for functions and descriptive comments

## Project Structure
- `main.py`: Core application with NiceGUI implementation
- `phrases.txt`: Contains customizable bingo phrases
- `static/`: Static assets for fonts and styles
- `helm/`: Kubernetes deployment configuration