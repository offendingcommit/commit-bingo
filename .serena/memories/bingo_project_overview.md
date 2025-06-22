# Bingo Project Overview

## Purpose
A customizable bingo board generator built with NiceGUI and Python. Creates interactive bingo games for streams, meetings, or events with shareable view-only links.

## Tech Stack
- **Language**: Python 3.12+
- **UI Framework**: NiceGUI (reactive web UI)
- **Package Manager**: Poetry
- **Testing**: pytest with coverage
- **Linting**: flake8, black, isort, mypy
- **Containerization**: Docker
- **Orchestration**: Kubernetes with Helm charts
- **CI/CD**: GitHub Actions with semantic-release
- **Web Server**: FastAPI (via NiceGUI)

## Project Structure
- `app.py`: Main entry point (modular structure)
- `main.py`: Legacy monolithic entry point
- `src/`: Source code
  - `config/`: Configuration and constants
  - `core/`: Core game logic
  - `ui/`: UI components (routes, sync, controls, board)
  - `utils/`: Utilities (file operations, text processing)
  - `types/`: Type definitions
- `tests/`: Unit and integration tests
- `phrases.txt`: Customizable bingo phrases
- `static/`: Static assets (fonts)
- `helm/`: Kubernetes deployment configs

## Key Features
- Custom phrases from file
- Shareable view-only boards
- Interactive click-to-mark tiles
- Stream integration support
- Responsive design
- State persistence
- Real-time synchronization between views

## Environment Variables
- `PORT`: Port number (default: 8080)
- `HOST`: Host address (default: 0.0.0.0)
- `DEBUG`: Debug mode (default: False)