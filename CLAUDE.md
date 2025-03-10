# Spinner Project Guidelines

## Development Commands
### Using Poetry (recommended)
- Run app: `poetry run python app.py`
- Install dependencies: `poetry install`
- Lint: `poetry run flake8 app.py config.py`
- Type check: `poetry run mypy app.py config.py`

### Using pip (legacy)
- Run app: `python app.py`
- Install dependencies: `pip install -r requirements.txt`
- Lint: `flake8 app.py config.py`
- Type check: `mypy app.py config.py`

## Environment Variables
All configuration options can be set through environment variables, such as:
- `WHEEL_COLOR_MODE=CUSTOM` - Sets the color mode (RGB or CUSTOM)
- `WHEEL_CUSTOM_COLORS='#FF0000,#00FF00,#0000FF'` - Sets custom colors (comma-separated)
- `WHEEL_TEXT_DISTANCE=0.8` - Sets text distance from center (0-1)
- `WHEEL_MARKER_ICON=arrow_circle_right` - Sets the marker icon
- See `config.py` for a complete list of available options

## Color Modes
- **RGB**: Generates colors across spectrum based on HSV (default)
- **CUSTOM**: Alternates between predefined hex values

## Code Style Guidelines
- **Formatting**: Follow PEP 8 standards
- **Imports**: Group standard library, third-party, and local imports
- **Types**: Use type hints for function parameters and return values
- **Naming Conventions**: Use CamelCase for classes, snake_case for functions/variables
- **Error Handling**: Use try/except blocks with specific exceptions

## Project Structure
- `app.py`: Main application file with NiceGUI interface
- `config.py`: Configuration system with environment variable support
- `options.txt`: Text file containing options for the spinner
- `CONTEXT.md`: Detailed documentation about project implementation
- `CLAUDE.md`: Project guidelines and commands (this file)
- `pyproject.toml`: Poetry project configuration
- `poetry.lock`: Poetry lock file with exact dependency versions
- `requirements.txt`: Legacy pip project dependencies

## Project Context
For detailed information about the project implementation, features, and technical details, please refer to the [CONTEXT.md](./CONTEXT.md) file.