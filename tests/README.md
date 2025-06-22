# Test Suite Organization

## Test Categories and Markers

### Speed/Scope Categories
- `@pytest.mark.unit` - Fast, isolated tests with no I/O or external dependencies
- `@pytest.mark.integration` - Tests requiring multiple components working together
- `@pytest.mark.e2e` - Full end-to-end tests with browser automation

### Component Categories
- `@pytest.mark.state` - StateManager functionality tests
- `@pytest.mark.game_logic` - Game rules and logic tests
- `@pytest.mark.ui` - UI component and rendering tests
- `@pytest.mark.persistence` - State persistence tests
- `@pytest.mark.sync` - View synchronization tests

### Characteristic Categories
- `@pytest.mark.slow` - Tests taking >1 second
- `@pytest.mark.flaky` - Tests that may fail intermittently
- `@pytest.mark.requires_app` - Tests needing NiceGUI app running
- `@pytest.mark.playwright` - Browser automation tests

### Special Categories
- `@pytest.mark.smoke` - Critical functionality tests
- `@pytest.mark.regression` - Bug fix verification tests
- `@pytest.mark.performance` - Performance measurement tests

## Test File Classification

### Pure Unit Tests (Fast)
- `test_game_logic.py` - Game rules, win conditions
- `test_state_manager.py` - StateManager isolation tests
- `test_helpers.py` - Utility function tests
- `test_file_operations.py` - File I/O utilities

### Integration Tests (Medium)
- `test_board_builder.py` - UI component integration
- `test_ui_functions.py` - UI behavior tests
- `test_state_persistence.py` - Persistence integration
- `test_integration.py` - General integration tests

### E2E Tests (Slow)
- `test_hot_reload_integration*.py` - Playwright browser tests
- `test_multi_session_*.py` - Multi-user scenarios
- `test_*_bdd.py` - Behavior-driven scenarios

## Running Tests by Category

```bash
# Run only fast unit tests
pytest -m unit

# Run unit and integration tests (no browser tests)
pytest -m "unit or integration"

# Run everything except slow tests
pytest -m "not slow"

# Run only StateManager tests
pytest -m state

# Run smoke tests for quick validation
pytest -m smoke

# Run tests for a specific component
pytest -m "game_logic and unit"
```

## Makefile Integration

```makefile
test-unit:
	poetry run pytest -m unit

test-integration:
	poetry run pytest -m integration

test-quick:
	poetry run pytest -m "unit or (integration and not slow)"

test-e2e:
	poetry run pytest -m e2e

test-smoke:
	poetry run pytest -m smoke
```