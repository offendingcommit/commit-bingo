# BINGO Project Guide

## Build Commands
```bash
# Quick setup for development
./setup.sh

# Install dependencies
poetry install

# Run application (old monolithic structure)
poetry run python main.py

# Run application (new modular structure)
poetry run python app.py

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src --cov-report=html

# Lint code
poetry run flake8
poetry run black --check .
poetry run isort --check .

# Format code
poetry run black .
poetry run isort .

# Build Docker container
docker build -t bingo .

# Run Docker container
docker run -p 8080:8080 bingo

# Helm deployment
cd helm && ./package.sh && helm install bingo ./bingo

# Using Makefile
make install  # Install dependencies
make run      # Run application
make test     # Run tests
make lint     # Run linters
make format   # Format code
make build    # Build package
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
- **Line Length**: Max 88 characters (Black's default)
- **Code Formatting**: Use Black for code formatting and isort for import sorting

## Project Structure
- `app.py`: Main entry point for modular application
- `src/`: Source code directory
  - `config/`: Configuration and constants
  - `core/`: Core game logic
  - `ui/`: User interface components
  - `utils/`: Utility functions
- `phrases.txt`: Contains customizable bingo phrases
- `static/`: Static assets for fonts and styles
- `tests/`: Unit and integration tests
- `helm/`: Kubernetes deployment configuration
- `.github/workflows/`: CI pipeline configuration
- `CHANGELOG.md`: Release history tracking

## Git Workflow

### Branch Naming
- Use feature branches for each change: `feature/description-of-change`
- Use bugfix branches for bug fixes: `fix/description-of-bug`
- Use chore branches for maintenance: `chore/description-of-task`

### Commit Guidelines
Follow conventional changelog format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

1. **Types**:
   - `feat`: A new feature
   - `fix`: A bug fix
   - `docs`: Documentation only changes
   - `style`: Changes that do not affect meaning (white-space, formatting)
   - `refactor`: Code change that neither fixes a bug nor adds a feature
   - `perf`: Change that improves performance
   - `test`: Adding missing tests or correcting existing tests
   - `chore`: Changes to the build process or auxiliary tools

2. **Scope** (optional): The module/component affected, e.g., `core`, `ui`, `board`

3. **Subject**: Short description in imperative, present tense (not past tense)
   - Good: "add feature X" (not "added feature X")
   - Use lowercase
   - No period at the end

4. **Body** (optional): Detailed explanation of changes
   - Use present tense
   - Include motivation and context
   - Explain "what" and "why" (not "how")

5. **Footer** (optional): Reference issues, PRs, breaking changes

### Example Commits:
```
feat(board): add color theme selector 

Add ability for users to choose color themes for the bingo board

Resolves #123
```

```
fix(ui): resolve client disconnection issues

Handle race conditions during client disconnects to prevent 
server exceptions and ensure smooth reconnection

Fixes #456
```

## Semantic Versioning

This project follows semantic versioning (SEMVER) principles:

- **MAJOR** version when making incompatible API changes (X.0.0)
- **MINOR** version when adding functionality in a backwards compatible manner (0.X.0)
- **PATCH** version when making backwards compatible bug fixes (0.0.X)

Version numbers are automatically updated by the CI/CD pipeline based on commit messages.
The project uses python-semantic-release to analyze commit messages and determine the appropriate 
version bump according to the conventional commit format.

## CI/CD Pipeline

The project utilizes GitHub Actions for continuous integration and deployment:

1. **CI Job**:
   - Runs on each push to main and pull request
   - Installs dependencies
   - Runs linters (flake8, black, isort)
   - Runs all tests with pytest
   - Uploads coverage reports

2. **Release Job**:
   - Runs after successful CI job on the main branch
   - Determines new version based on commit messages
   - Updates CHANGELOG.md
   - Creates Git tag for the release
   - Publishes release on GitHub