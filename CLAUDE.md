# Spinner Project Guidelines

## Development Commands
### Using Poetry
- Run app: `poetry run python app.py`
- Install dependencies: `poetry install`
- Lint: `poetry run flake8 app.py`
- Type check: `poetry run mypy app.py`

### Using pip (legacy)
- Run app: `python app.py`
- Install dependencies: `pip install -r requirements.txt`
- Lint: `flake8 app.py`
- Type check: `mypy app.py`

## Code Style Guidelines
- **Formatting**: Follow PEP 8 standards
- **Imports**: Group standard library, third-party, and local imports
- **Types**: Use type hints for function parameters and return values
- **Naming Conventions**: Use CamelCase for classes, snake_case for functions/variables
- **Error Handling**: Use try/except blocks with specific exceptions

## Project Structure
- `app.py`: Main application file with NiceGUI interface
- `names.txt`: Text file containing names for the spinner
- `pyproject.toml`: Poetry project configuration
- `poetry.lock`: Poetry lock file with exact dependency versions
- `requirements.txt`: Legacy pip project dependencies