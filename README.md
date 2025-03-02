# Bingo Board Generator

A customizable bingo board generator built with NiceGUI and Python.

## Features

- Generate interactive 5x5 bingo boards
- Customizable phrases from phrases.txt file
- Automatic text sizing to fit all content
- Real-time detection of win patterns
- Support for different views (home and stream)
- Mobile-friendly responsive design

## Installation

1. Clone the repository

2. Install dependencies with Poetry:
```bash
poetry install
```

3. Run the application:
```bash
python app.py
```

The application will be available at http://localhost:8080

## Docker

You can also run the application using Docker:

```bash
docker build -t bingo .
docker run -p 8080:8080 bingo
```

## Testing

Run tests with pytest:

```bash
poetry run pytest
```

Or for full coverage report:

```bash
poetry run pytest --cov=src --cov-report=html
```

## Project Structure

- `app.py`: Main entry point for the application
- `src/`: Source code directory
  - `config/`: Configuration and constants
  - `core/`: Core game logic
  - `ui/`: User interface components
  - `utils/`: Utility functions
- `tests/`: Unit tests
- `static/`: Static assets (fonts, etc.)
- `phrases.txt`: Customizable bingo phrases

## Customization

Modify the `phrases.txt` file to add your own bingo phrases. The application will reload them automatically.