# BINGO Project Guide

## Project Overview

**Commit Bingo** is a customizable bingo board generator built with NiceGUI and Python. It's designed for streamers, meetings, and events with real-time state synchronization and persistent game state.

- **Current Version**: 1.2.1
- **Python Version**: 3.12+
- **Framework**: NiceGUI 2.11.0+
- **License**: MIT
- **Repository**: https://github.com/offendingcommit/commit-bingo

## Quick Start

```bash
# Quick setup for development
./setup.sh

# Or manual setup
poetry install
poetry run python app.py
```

## Build Commands

```bash
# Quick setup for development
./setup.sh

# Install dependencies
poetry install

# Run application (old monolithic structure)
poetry run python main.py

# Run application (new modular structure - RECOMMENDED)
poetry run python app.py

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test categories (see Test Suite section)
make test-unit       # Fast unit tests only
make test-quick      # Unit + fast integration
make test-smoke      # Critical functionality only

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
make test     # Run all tests
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

```
commit-bingo/
├── app.py                    # Main entry point (modular architecture) - RECOMMENDED
├── main.py                   # Legacy entry point (monolithic) - kept for compatibility
├── pyproject.toml           # Poetry dependencies and project configuration
├── poetry.lock              # Locked dependency versions
├── Dockerfile               # Container image definition
├── Makefile                 # Build automation and common commands
├── setup.sh                 # Quick development environment setup
├── phrases.txt              # Customizable bingo phrases (one per line)
├── .flake8                  # Linter configuration
├── pytest.ini               # Test configuration and markers
├── CLAUDE.md                # This file - AI assistant guide
├── README.md                # User-facing documentation
├── CHANGELOG.md             # Semantic release history
├── LICENSE                  # MIT license
│
├── src/                     # Source code (modular architecture)
│   ├── config/
│   │   ├── __init__.py
│   │   └── constants.py     # UI colors, fonts, messages, CSS classes
│   ├── core/
│   │   ├── __init__.py
│   │   ├── game_logic.py    # Game state, win conditions, board generation
│   │   └── state_manager.py # Server-side persistence (replaces client storage)
│   ├── types/
│   │   ├── __init__.py
│   │   └── ui_types.py      # Type definitions for game components
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── board_builder.py # Board rendering and tile creation
│   │   ├── controls.py      # Control buttons (reset, new game, close)
│   │   ├── head.py          # HTML head with fonts and styles
│   │   ├── routes.py        # NiceGUI route definitions (/, /stream, /health)
│   │   └── sync.py          # Timer-based view synchronization
│   └── utils/
│       ├── __init__.py
│       ├── file_monitor.py  # Watch phrases.txt for changes
│       ├── file_operations.py # Read/write phrase files
│       └── text_processing.py # Phrase formatting and line wrapping
│
├── tests/                   # Comprehensive test suite
│   ├── README.md            # Test organization and markers guide
│   ├── README_multi_session_tests.md
│   ├── features/            # BDD feature files
│   ├── test_*_unit.py       # Fast unit tests (no I/O)
│   ├── test_*_integration.py # Component integration tests
│   ├── test_*_bdd.py        # Behavior-driven tests
│   ├── test_state_manager.py # StateManager isolation tests
│   ├── test_game_logic.py    # Game rules and logic
│   ├── test_board_builder.py # UI component tests
│   ├── test_ui_functions.py  # UI behavior tests
│   └── test_hot_reload_*.py  # Browser automation (Playwright)
│
├── static/                  # Static assets
│   └── fonts/               # Custom fonts (Super Carnival, etc.)
│
├── helm/                    # Kubernetes deployment
│   └── bingo/
│       ├── Chart.yaml       # Helm chart metadata
│       ├── values.yaml      # Configuration values
│       └── templates/       # K8s resource templates
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── ingress.yaml
│           ├── configmap.yaml
│           ├── pvc.yaml     # Persistent volume for state
│           ├── hpa.yaml     # Horizontal pod autoscaling
│           └── serviceaccount.yaml
│
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI: lint, test, coverage
│       └── release-pipeline.yml # Semantic release automation
│
├── .serena/                 # Code intelligence (Serena MCP)
│   ├── project.yml
│   └── memories/            # Project knowledge and patterns
│
└── scripts/
    └── tag_tests.py         # Utility to tag tests with markers
```

### Key Files

- **app.py** (82 lines): Modern entry point using modular architecture from `src/`
- **main.py** (497 lines): Legacy monolithic version, kept for backward compatibility
- **src/core/state_manager.py** (294 lines): Server-side state persistence with async operations
- **src/core/game_logic.py** (497 lines): Game state, board generation, win detection
- **src/config/constants.py** (55 lines): All configuration values and styling constants
- **game_state.json**: Runtime state file (gitignored, auto-created)

### Important Patterns

1. **Entry Point**: Use `app.py` for new development (modular architecture)
2. **State Management**: All state operations go through `StateManager` singleton
3. **UI Routes**: Three routes defined in `src/ui/routes.py`:
   - `/` - Interactive board (main view)
   - `/stream` - Read-only board (for audience)
   - `/health` - Health check endpoint
4. **Synchronization**: Timer-based updates (50ms interval) instead of deprecated `ui.broadcast()`

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

## Pre-Push Checklist

Before pushing changes to the repository, run these checks locally to ensure the CI pipeline will pass:

```bash
# 1. Run linters to ensure code quality and style
poetry run flake8 main.py src/ tests/
poetry run black --check .
poetry run isort --check .

# 2. Run tests to ensure functionality works
poetry run pytest

# 3. Check test coverage to ensure sufficient testing
poetry run pytest --cov=main --cov-report=term-missing

# 4. Fix any linting issues
poetry run black .
poetry run isort .

# 5. Run tests again after fixing linting issues
poetry run pytest

# 6. Verify application starts without errors
poetry run python main.py  # (Ctrl+C to exit after confirming it starts)
```

### Common CI Failure Points to Check:

1. **Code Style Issues**:
   - Inconsistent indentation
   - Line length exceeding 88 characters
   - Missing docstrings
   - Improper import ordering

2. **Test Failures**:
   - Broken functionality due to recent changes
   - Missing tests for new features
   - Incorrectly mocked dependencies in tests
   - Race conditions in async tests

3. **Coverage Thresholds**:
   - Insufficient test coverage on new code
   - Missing edge case tests
   - Uncovered exception handling paths

### Quick Fix Command Sequence

If you encounter CI failures, this sequence often resolves common issues:

```bash
# Fix style issues
poetry run black .
poetry run isort .

# Run tests with coverage to identify untested code
poetry run pytest --cov=main --cov-report=term-missing

# Add tests for any uncovered code sections then run again
poetry run pytest
```

## Test Suite Organization

The project has a comprehensive test suite with **pytest markers** for selective test execution.

### Test Categories and Markers

#### Speed/Scope Categories
- `@pytest.mark.unit` - Fast, isolated tests with no I/O or external dependencies (~5 seconds for all)
- `@pytest.mark.integration` - Tests requiring multiple components working together
- `@pytest.mark.e2e` - Full end-to-end tests with browser automation (Playwright)

#### Component Categories
- `@pytest.mark.state` - StateManager functionality tests
- `@pytest.mark.game_logic` - Game rules and logic tests
- `@pytest.mark.ui` - UI component and rendering tests
- `@pytest.mark.persistence` - State persistence tests
- `@pytest.mark.sync` - View synchronization tests

#### Characteristic Categories
- `@pytest.mark.slow` - Tests taking >1 second
- `@pytest.mark.flaky` - Tests that may fail intermittently (excluded from CI)
- `@pytest.mark.requires_app` - Tests needing NiceGUI app running
- `@pytest.mark.playwright` - Browser automation tests (excluded from CI)

#### Special Categories
- `@pytest.mark.smoke` - Critical functionality tests
- `@pytest.mark.regression` - Bug fix verification tests
- `@pytest.mark.performance` - Performance measurement tests

### Running Tests by Category

```bash
# Progressive test execution (fastest to slowest)
make test-unit           # ~5s - Run only fast unit tests
make test-quick          # ~15s - Unit + fast integration
make test                # ~30s - All tests except e2e/slow/flaky
make test-e2e            # ~2min - Full browser automation tests

# Component-specific tests
make test-state          # StateManager tests only
make test-ui             # UI component tests
make test-persistence    # State persistence tests

# Special test modes
make test-smoke          # Critical functionality only
make test-failed         # Re-run only failed tests
make test-watch          # Continuous testing (unit tests)

# Advanced filtering with pytest
pytest -m unit                           # Unit tests only
pytest -m "unit or integration"          # Combined categories
pytest -m "state and unit"               # StateManager unit tests
pytest -m "not slow and not flaky"       # Exclude unreliable tests
pytest -m "smoke"                        # Critical tests only
pytest --lf                              # Last failed
pytest -x                                # Stop on first failure
pytest -k "test_toggle"                  # Tests matching name pattern
```

### Test File Organization

```
tests/
├── README.md                          # Test organization guide (detailed)
├── test_helpers.py                    # Test utilities
│
├── Unit Tests (Fast, <5s total)
│   ├── test_game_logic_unit.py        # Game logic isolation
│   ├── test_file_operations_unit.py   # File I/O utilities
│   └── test_text_processing_unit.py   # Text formatting
│
├── Component Tests
│   ├── test_state_manager.py          # StateManager (96% coverage)
│   ├── test_game_logic.py             # Game integration
│   ├── test_board_builder.py          # UI components
│   └── test_ui_functions.py           # UI behavior
│
├── Integration Tests
│   ├── test_state_persistence.py      # State persistence integration
│   ├── test_state_persistence_bdd.py  # BDD scenarios
│   ├── test_state_persistence_bugs.py # Regression tests
│   ├── test_state_persistence_issues.py
│   └── test_integration.py            # General integration
│
└── E2E Tests (Slow, browser automation)
    ├── test_hot_reload_integration.py
    ├── test_hot_reload_integration_improved.py
    ├── test_hot_reload_manual.py
    ├── test_multi_session_simple.py
    ├── test_multi_session_bdd.py
    └── test_multi_session_responsiveness.py
```

### CI Test Execution

The CI pipeline runs a **curated set of fast, reliable tests** (~7 seconds):

```yaml
# CI runs these tests (from .github/workflows/ci.yml)
poetry run pytest tests/test_*_unit.py -v  # Unit tests first
poetry run pytest --cov=src -m "not e2e and not playwright and not slow and not integration and not flaky"
```

**Why tests are excluded from CI:**
- **e2e/playwright**: Require browser binaries (Playwright) not installed in CI environment
- **slow**: Performance tests that take >1s each
- **integration**: Multi-session tests with timing dependencies
- **flaky**: Tests with intermittent failures due to timing or async issues

**Total test count:**
- All tests: ~165 tests
- CI tests: ~139 tests (26 excluded for reliability)
- Unit tests only: ~79 tests

### Writing New Tests

When adding tests, **always add appropriate markers**:

```python
import pytest

@pytest.mark.unit
@pytest.mark.game_logic
def test_board_generation():
    """Fast, isolated test of board generation logic."""
    pass

@pytest.mark.integration
@pytest.mark.state
@pytest.mark.slow
def test_state_persistence_across_sessions():
    """Integration test requiring file I/O and multiple components."""
    pass

@pytest.mark.e2e
@pytest.mark.playwright
@pytest.mark.ui
@pytest.mark.flaky
async def test_multi_browser_sync():
    """Browser automation test - may be timing-sensitive."""
    pass
```

### Test Coverage Goals

- **StateManager**: 96% coverage (comprehensive unit tests)
- **Overall src/**: Aim for >80% coverage
- **New features**: Must include unit tests
- **Bug fixes**: Add regression tests with `@pytest.mark.regression`

## Testing Game State Synchronization

Special attention should be paid to testing game state synchronization between the main view and the stream view:

```bash
# Run specific tests for state synchronization
poetry run pytest -v tests/test_ui_functions.py::TestUIFunctions::test_header_updates_on_both_paths
poetry run pytest -v tests/test_ui_functions.py::TestUIFunctions::test_stream_header_update_when_game_closed
```

When making changes to game state management, especially related to:
- Game closing/reopening
- Header text updates
- Board visibility
- Broadcast mechanisms

Verify both these scenarios:
1. Changes made on main view are reflected in stream view
2. Changes persist across page refreshes
3. New connections to stream page see the correct state

Common issues:
- Missing ui.broadcast() calls
- Not handling header updates across different views
- Not checking if game is closed in sync_board_state
- Ignoring exception handling for disconnected clients

## State Persistence (Quick Reference)

See **Architecture & Key Decisions** section for comprehensive details.

**StateManager Singleton:**
```python
from src.core.state_manager import get_state_manager
state_manager = get_state_manager()
```

**Key Operations:**
```python
# Async operations (all trigger automatic save)
await state_manager.toggle_tile(row, col)
await state_manager.update_board(board, iteration, seed)
await state_manager.set_game_closed(True)
await state_manager.update_header_text("New Text")
await state_manager.reset_board()

# Read-only properties
tiles = state_manager.clicked_tiles      # Returns copy
closed = state_manager.is_game_closed
iter = state_manager.board_iteration
```

**State File:**
- Location: `game_state.json` (gitignored)
- Format: JSON with serialized Python types
- Persistence: Automatic debounced saves (500ms delay)
- Atomicity: Temp file + rename pattern
- Recovery: Graceful handling of corrupted files

**Testing:**
- Test file: `tests/test_state_manager.py`
- Coverage: 96%
- Markers: `@pytest.mark.state`, `@pytest.mark.unit`
## View Synchronization

The application maintains two synchronized views:

### Views
- **Root Path (`/`)**: Full interactive board with controls
- **Stream Path (`/stream`)**: Read-only view for audiences

### Synchronization Strategy
- **Timer-based**: Uses 0.05 second interval timers
- **NiceGUI 2.11+ Compatible**: Removed deprecated `ui.broadcast()`
- **Automatic Updates**: UI changes propagate to all connected clients
- **State Consistency**: Both views share same game state

### User Tracking
- Active connections tracked per path
- Connection/disconnection handled gracefully
- Health endpoint reports user counts
- UI displays active user count

## NiceGUI Framework Notes

### Version Compatibility
- Built for NiceGUI 2.11.0+
- Uses `app.storage.general` for persistence
- Timer-based synchronization pattern
- No longer uses deprecated `ui.broadcast()`

### Storage Best Practices
```python
# Store data
app.storage.general['key'] = value

# Retrieve with default
value = app.storage.general.get('key', default_value)

# Check existence
if 'key' in app.storage.general:
    # process
```

### UI Patterns
- Buttons support text + icons for mobile
- Use context managers for UI containers
- Handle disconnected clients in try/except
- Timer callbacks for periodic updates

### Mobile Optimization
- Touch targets: minimum 44x44 pixels
- Descriptive text alongside icons
- Responsive design classes
- Clear visual feedback

## Docker & Deployment

### Docker

The project includes a production-ready Dockerfile:

```dockerfile
# Key features:
- Base image: python:3.12-slim
- Poetry 1.8.3 for dependency management
- Non-root user (appuser) for security
- Health check endpoint at /health
- Port 8080 exposed
- Multi-stage caching for faster builds
```

**Build and run:**

```bash
# Build
docker build -t bingo .

# Run locally
docker run -p 8080:8080 bingo

# Run with custom storage secret
docker run -p 8080:8080 -e STORAGE_SECRET="your-secret-here" bingo

# Production build (no dev dependencies)
docker build --build-arg BUILD_ENVIRONMENT=production -t bingo:prod .
```

**Health Check:**
- Endpoint: `http://localhost:8080/health`
- Interval: 30 seconds
- Timeout: 5 seconds
- Retries: 3

### Kubernetes (Helm)

The project includes Helm charts for Kubernetes deployment:

```bash
# Package and install
cd helm
./package.sh
helm install bingo ./bingo

# Custom values
helm install bingo ./bingo -f custom-values.yaml

# Upgrade
helm upgrade bingo ./bingo

# Uninstall
helm uninstall bingo
```

**Included resources:**
- **Deployment**: Application pods with configurable replicas
- **Service**: ClusterIP service on port 80 → 8080
- **Ingress**: Optional ingress for external access
- **ConfigMap**: Configuration for phrases and settings
- **PersistentVolumeClaim**: For game_state.json persistence
- **HorizontalPodAutoscaler**: Auto-scaling based on CPU/memory
- **ServiceAccount**: RBAC configuration

**Key configuration (values.yaml):**
```yaml
replicaCount: 2
image:
  repository: bingo
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: false
  className: nginx

persistence:
  enabled: true
  size: 1Gi
  storageClass: ""

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPU: 80
```

**Important for state persistence:**
- Enable PVC to persist `game_state.json` across pod restarts
- Mount path: `/app/game_state.json`
- Without PVC, state resets when pods restart

### Environment Variables

```bash
STORAGE_SECRET    # NiceGUI storage encryption key (default: "ThisIsMyCrappyStorageSecret")
PORT              # Server port (default: 8080)
HOST              # Server host (default: 0.0.0.0)
DEBUG             # Debug mode (default: False)
```

## Dependencies

### Production Dependencies
```toml
python = "^3.12"       # Modern Python features and performance
nicegui = "^2.11.0"   # Web UI framework
toml = "^0.10.2"      # Configuration file parsing
```

### Development Dependencies
```toml
pytest = "^7.4.0"               # Test framework
pytest-cov = "^4.1.0"           # Coverage reporting
pytest-bdd = "^8.1.0"           # Behavior-driven testing
pytest-asyncio = "<1.0"         # Async test support
playwright = "^1.52.0"          # Browser automation for E2E tests
flake8 = "^7.0.0"              # Linting
black = "^24.2.0"              # Code formatting
isort = "^5.13.2"              # Import sorting
mypy = "^1.15.0"               # Type checking (configured but not enforced)
python-semantic-release = "^9.1.1"  # Automated versioning
```

**Note**: Black is excluded from CI due to architecture compatibility issues on some platforms.

## Architecture & Key Decisions

### Evolution Timeline

#### v1.0.x - Initial Release
- Monolithic `main.py` with all code in one file
- Client-side state with `app.storage.general` (browser localStorage)
- Basic synchronization with `ui.broadcast()`

#### v1.1.x - Modularization
- Split code into `src/` modules (config, core, ui, utils, types)
- Introduced `app.py` as modern entry point
- Kept `main.py` for backward compatibility

#### v1.2.x - State Persistence (Current)
- **v1.2.0**: StateManager pattern for server-side persistence
- **v1.2.1**: Test infrastructure improvements and CI optimization

### StateManager Architecture (v1.2.0+)

**Problem**: `app.storage.general` uses browser localStorage, which:
- Doesn't persist across server restarts
- Is client-side only (not shared across browser sessions)
- Can't be backed up or migrated easily

**Solution**: Server-side StateManager pattern

```python
# src/core/state_manager.py
class GameStateManager:
    """Server-side state management with file persistence."""

    # Features:
    - Singleton pattern for global access
    - Async operations with proper locking (thread-safe)
    - Debounced saves (500ms delay) to reduce I/O
    - Atomic writes using temp file + rename
    - Automatic state loading on app startup
    - Corrupted state recovery

    # State file: game_state.json (gitignored)
    {
        "board": [[...], ...],           # 5x5 grid of phrases
        "clicked_tiles": [[r, c], ...],  # Clicked positions
        "bingo_patterns": ["row0", ...], # Winning patterns found
        "is_game_closed": false,
        "board_iteration": 1,            # Board version
        "today_seed": "20250626.1",
        "header_text": "BINGO!",
        "timestamp": 1719417600.0
    }
```

**Usage Pattern:**

```python
from src.core.state_manager import get_state_manager

# Get singleton instance
state_manager = get_state_manager()

# Async operations (from NiceGUI callbacks)
await state_manager.toggle_tile(row, col)
await state_manager.update_board(board, iteration, seed)
await state_manager.set_game_closed(True)
await state_manager.update_header_text("New Header")
await state_manager.reset_board()

# Read-only properties
clicked_tiles = state_manager.clicked_tiles  # Returns copy
is_closed = state_manager.is_game_closed
board_iter = state_manager.board_iteration

# Get full state as dict
state_dict = state_manager.get_full_state()
```

**Migration from app.storage.general:**

```python
# OLD WAY (client-side, doesn't persist):
app.storage.general['clicked_tiles'] = list(clicked_tiles)
clicked = app.storage.general.get('clicked_tiles', [])

# NEW WAY (server-side, persists):
await state_manager.update_board(board, iteration, seed)
clicked = state_manager.clicked_tiles
```

### View Synchronization Strategy

**Evolution:**
1. **v1.0.x**: Used `ui.broadcast()` for cross-client updates
2. **v1.1.x**: `ui.broadcast()` deprecated in NiceGUI 2.11+
3. **v1.2.x**: Timer-based synchronization (current approach)

**Current Implementation:**

```python
# src/ui/sync.py
@ui.timer(0.05)  # 50ms interval (20 updates/second)
async def sync_board_state():
    """Synchronize board state across all connected clients."""
    # Updates UI elements based on current state
    # Runs on all clients independently
    # No manual broadcasting needed
```

**Two views:**
- `/` - Interactive board (main view) with controls
- `/stream` - Read-only board for audience/viewers

Both views share the same `board_views` dictionary and synchronize via timers.

### Game Logic Patterns

**Win Conditions:**
- Standard: 5 rows + 5 columns + 2 diagonals = 12 possible
- Special: Blackout, 4 Corners, Plus, X-shape, Perimeter
- Multi-bingo: Double, Triple, Quadruple, Quintuple, N-way

**Board Generation:**
```python
# Deterministic seeding for reproducibility
seed = f"{date}.{iteration}"  # e.g., "20250626.1"
random.seed(iteration)
board = generate_board(iteration, phrases)
```

**Free Space:**
- Always at position (2, 2) - center of 5x5 grid
- Always pre-clicked
- Cannot be toggled
- Text: "FREE MEAT" (customizable in constants.py)

### UI/UX Design Decisions

**Fitty.js Integration:**
- Auto-sizing text to fit tiles
- Multi-line support for long phrases
- Applied via JavaScript after tile updates

**Responsive Design:**
- Tailwind CSS classes for layouts
- Grid-based 5x5 board using CSS grid
- Minimum touch target: 44x44px (mobile-friendly)

**Color Scheme (constants.py):**
```python
TILE_UNCLICKED_BG_COLOR = "#1BEFF5"   # Cyan background
TILE_UNCLICKED_TEXT_COLOR = "#100079"  # Dark purple text
TILE_CLICKED_BG_COLOR = "#100079"      # Dark purple background
TILE_CLICKED_TEXT_COLOR = "#1BEFF5"    # Cyan text (inverted)
```

### Testing Strategy Evolution

**v1.0.x**: Basic pytest tests, no markers
**v1.1.x**: Added integration tests, some markers
**v1.2.x**: Comprehensive marker system for selective execution

**Key insight from v1.2.0:**
- CI was timing out with all 165 tests
- Solution: Exclude slow/flaky/e2e tests from CI
- Result: CI runs 139 reliable tests in ~7s

**Test pyramid:**
```
        /\
       /E2E\       ~26 tests, ~2min (browser automation)
      /______\
     /        \
    /Integration\ ~50 tests, ~20s (multi-component)
   /____________\
  /              \
 /  Unit Tests    \ ~79 tests, ~5s (fast, isolated)
/__________________\
```

### File Organization Principles

1. **Separation of Concerns:**
   - `config/` - Constants and configuration (no logic)
   - `core/` - Business logic (game rules, state management)
   - `ui/` - Presentation layer (NiceGUI components)
   - `utils/` - Shared utilities (file I/O, text processing)
   - `types/` - Type definitions (for type hints)

2. **Entry Points:**
   - `app.py` - Modern, modular (82 lines)
   - `main.py` - Legacy, monolithic (497 lines) - kept for backward compatibility

3. **Test Organization:**
   - Mirror `src/` structure
   - Separate unit/integration/e2e files
   - Use markers for categorization

### Known Issues & Gotchas

1. **Black in CI**: Disabled due to ARM64 architecture issues on some runners
2. **Playwright Tests**: Require browser binaries, excluded from CI
3. **Timing Sensitivity**: Multi-session tests can be flaky due to async timing
4. **State File Lock**: StateManager uses asyncio locks, not process locks (single-process only)
5. **NiceGUI Storage**: Still uses `app.storage.general` for NiceGUI framework config, but NOT game state

### Performance Considerations

**StateManager Debouncing:**
- Saves delayed by 500ms to batch rapid updates
- Prevents excessive file I/O during rapid tile clicking
- Can override with `immediate=True` for critical saves

**UI Updates:**
- 50ms timer for synchronization (20 FPS)
- Fitty.js re-renders delayed by 50ms after updates
- Balance between responsiveness and CPU usage

**Test Execution:**
- Unit tests: <5 seconds (ideal for TDD)
- Quick tests: <15 seconds (pre-commit)
- Full CI: <30 seconds (automated)
- E2E tests: ~2 minutes (manual/nightly)

## MCP Tools & Memory Management

### 🛑 STOP! SAVE TO MEMORY NOW - NOT LATER!

#### THROUGHOUT EVERY SESSION:
- ✅ Just solved something? → SAVE NOW
- ✅ Created a script? → SAVE NOW  
- ✅ Fixed an error? → SAVE NOW
- ✅ Made a decision? → SAVE NOW
- ✅ Discovered a pattern? → SAVE NOW

**DON'T WAIT UNTIL THE END OF THE SESSION!**

### Memory-First Protocol (CRITICAL)
- **ALWAYS** search memory BEFORE starting any work: `mcp__mcp-memory__searchMCPMemory "bingo [topic]"`
- **ALWAYS** save solutions after fixing issues: `mcp__mcp-memory__addToMCPMemory "bingo: Problem: X, Solution: Y"`
- **Save context switches**: When interrupted or switching tasks, save current state
- **Capture train of thought**: Document reasoning and decision paths

### Memory Save Triggers (DO IMMEDIATELY)
- After creating any script → Save its purpose and usage
- After fixing any error → Save problem + solution  
- After file reorganization → Save what moved where
- After discovering pattern → Save the insight
- After making decision → Save the rationale
- After solving problem → Save approach + result

### Session Start Protocol for Bingo
```bash
# 1. Restore context from last session
mcp__mcp-memory__searchMCPMemory "bingo last session state"
mcp__mcp-memory__searchMCPMemory "bingo open tasks TODO"
mcp__mcp-memory__searchMCPMemory "Jonathan workflow guidelines best practices"

# 2. Rebuild mental model
tree . -I 'node_modules' -L 2
cat CLAUDE.md

# 3. Load comprehensive project memory
mcp__mcp-memory__searchMCPMemory "bingo current state"
mcp__mcp-memory__searchMCPMemory "bingo where I left off"
mcp__mcp-memory__searchMCPMemory "bingo blockers questions"
mcp__mcp-memory__searchMCPMemory "bingo solutions patterns"
mcp__mcp-memory__searchMCPMemory "bingo nicegui patterns"
mcp__mcp-memory__searchMCPMemory "bingo state persistence"
mcp__mcp-memory__searchMCPMemory "bingo testing infrastructure"

# 4. Check work state
git status
git diff
git log --oneline -10
gh pr list --assignee @me --state open
```

### MCP Tools Available

1. **mcp-memory** (Always Active - External Brain)
   - `mcp__mcp-memory__searchMCPMemory "[query]"` - Search stored knowledge
   - `mcp__mcp-memory__addToMCPMemory "content"` - Save new knowledge
   - Always prefix with "bingo:" for project isolation

2. **sequentialthinking** - For complex reasoning (especially with Sonnet 4)
   - Use for architectural decisions and complex debugging
   - Saves reasoning process to memory automatically

3. **context7** (Documentation lookup)
   - `mcp__context7__resolve-library-id`: Find library IDs (e.g., NiceGUI)
   - `mcp__context7__get-library-docs`: Get library documentation

4. **serena** (Code intelligence)
   - Activate with: `mcp__serena__activate_project "bingo"`
   - Provides symbol search, refactoring, and code analysis

### Memory Templates for Bingo Project

#### Error Solutions
```
Project: bingo
Error: [exact error message]
Context: [NiceGUI version, test environment, etc.]
Solution: [step-by-step fix]
Code Before: [relevant code showing issue]
Code After: [corrected code]
Validation: [how verified it worked]
Tags: bingo, error-fix, [component], [technology]
```

#### Testing Infrastructure
```
Project: bingo
Component: [StateManager/UI/Testing]
Issue: [what needed testing/fixing]
Approach: [testing strategy used]
Implementation: [specific test code/patterns]
Results: [coverage/performance metrics]
Patterns: [reusable testing patterns discovered]
Tags: bingo, testing, [unit/integration/e2e], [component]
```

#### NiceGUI Specific Patterns
```
Project: bingo
NiceGUI Pattern: [state management/UI/timers/etc.]
Problem: [what was challenging]
Solution: [NiceGUI-specific approach]
Code Example: [working implementation]
Gotchas: [things to watch out for]
Performance: [any performance considerations]
Tags: bingo, nicegui, [pattern-type], [version]
```

#### StateManager Architecture
```
Project: bingo
Architecture Decision: [what was decided]
Previous Approach: [old way - app.storage.general]
New Approach: [StateManager pattern]
Implementation: [key code/patterns]
Benefits: [persistence, thread-safety, etc.]
Testing Strategy: [how we verified it works]
Tags: bingo, architecture, state-persistence, statemanager
```

### Common Search Patterns for Bingo
```bash
# Starting work
mcp__mcp-memory__searchMCPMemory "bingo session startup protocol"
mcp__mcp-memory__searchMCPMemory "bingo current priorities"

# Debugging
mcp__mcp-memory__searchMCPMemory "bingo [error-type] solutions"
mcp__mcp-memory__searchMCPMemory "bingo nicegui [issue-type]"
mcp__mcp-memory__searchMCPMemory "bingo testing [test-type] patterns"

# Development
mcp__mcp-memory__searchMCPMemory "bingo statemanager patterns"
mcp__mcp-memory__searchMCPMemory "bingo ci optimization"
mcp__mcp-memory__searchMCPMemory "bingo deployment troubleshooting"
```

### What to Save for Bingo (SAVE IMMEDIATELY)
- **Every StateManager fix/enhancement** with before/after code
- **NiceGUI UI patterns** that work well for this app
- **Testing strategies** that prove effective (unit/integration/e2e)
- **CI/CD optimizations** and performance improvements
- **Docker/Helm deployment issues** and their solutions
- **Performance bottlenecks** and optimization approaches
- **User experience improvements** and their impact
- **Architecture decisions** with reasoning and alternatives considered

---

## Quick Reference Cheat Sheet

### Most Common Commands

```bash
# Development
poetry install              # First-time setup
poetry run python app.py    # Run application
make test-unit             # Quick test (5s)
make test-quick            # Pre-commit tests (15s)
make format                # Auto-format code
make lint                  # Check code quality

# Testing by component
pytest -m state            # StateManager tests
pytest -m game_logic       # Game logic tests
pytest -m ui               # UI component tests
pytest -k "test_toggle"    # Tests matching name

# Debugging
pytest -v -s               # Verbose with print output
pytest -x                  # Stop on first failure
pytest --lf                # Re-run last failed
pytest --pdb               # Drop into debugger on failure
```

### Project Locations

```
app.py                          # Modern entry point (USE THIS)
main.py                         # Legacy entry point

src/config/constants.py         # All UI constants (colors, fonts, text)
src/core/state_manager.py       # State persistence (singleton)
src/core/game_logic.py          # Game rules and win detection
src/ui/routes.py                # Route definitions (/, /stream, /health)
src/ui/board_builder.py         # Board rendering
src/ui/sync.py                  # Timer-based synchronization

tests/test_state_manager.py    # StateManager unit tests (96% coverage)
tests/README.md                 # Test organization guide

game_state.json                 # Runtime state (gitignored, auto-created)
phrases.txt                     # Bingo phrases (one per line)

.github/workflows/ci.yml        # CI pipeline
helm/bingo/                     # Kubernetes deployment
Dockerfile                      # Container image
```

### Common Tasks

**Add a new phrase:**
```bash
echo "New phrase here" >> phrases.txt
# App auto-reloads with file monitor
```

**Change UI colors:**
```python
# Edit src/config/constants.py
TILE_CLICKED_BG_COLOR = "#NEWCOLOR"
```

**Add a new win condition:**
```python
# Edit src/core/game_logic.py -> check_winner()
# Add pattern check, update bingo_patterns set
# Add corresponding test in tests/test_game_logic.py
```

**Debug state persistence:**
```bash
# Check state file
cat game_state.json | jq .

# Delete state file to reset
rm game_state.json

# Run StateManager tests
pytest tests/test_state_manager.py -v
```

**Run app in Docker:**
```bash
docker build -t bingo .
docker run -p 8080:8080 bingo
# Access at http://localhost:8080
```

### Key Concepts to Remember

1. **Always use StateManager** for game state (never `app.storage.general`)
2. **Timer-based sync** (not `ui.broadcast()`) for NiceGUI 2.11+
3. **Test markers** are required for all new tests
4. **app.py is preferred** over main.py for new development
5. **Free space** is always at (2, 2) and cannot be toggled
6. **Debounced saves** mean state writes are delayed by 500ms
7. **Two views** (/ and /stream) share the same state but different permissions
8. **CI excludes** slow/flaky/e2e/integration tests for speed

### Troubleshooting

**Tests failing in CI but passing locally:**
- Check for `@pytest.mark` on new tests
- Ensure no browser/playwright dependencies in unit tests
- Verify no timing-sensitive assertions

**State not persisting:**
- Check `game_state.json` exists and is writable
- Verify using `StateManager` not `app.storage.general`
- Look for exceptions in logs during save operations

**UI not synchronizing:**
- Verify timer in `src/ui/sync.py` is running
- Check that both views are in `board_views` dict
- Ensure no exceptions preventing timer execution

**Import errors:**
- Run `poetry install` to ensure dependencies are installed
- Check Python version is 3.12+
- Verify virtual environment is activated

**Linting failures:**
- Run `make format` to auto-fix most issues
- Check `.flake8` for ignored rules
- Note: Black is excluded from CI

### Version History Highlights

- **v1.2.1** (Current): Improved tests and CI optimization
- **v1.2.0**: StateManager for server-side persistence
- **v1.1.x**: Modular architecture with src/ split
- **v1.0.x**: Initial monolithic release

### Resources

- **NiceGUI Docs**: https://nicegui.io
- **Project README**: ./README.md
- **Test Guide**: ./tests/README.md
- **Changelog**: ./CHANGELOG.md
- **Issues**: https://github.com/offendingcommit/commit-bingo/issues

---

**End of CLAUDE.md** - Last updated: 2025-11-15 for version 1.2.1