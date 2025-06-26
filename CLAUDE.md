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

## State Persistence

The application uses a server-side StateManager for persistent state management:

### Architecture Update (2025-06-22)
- **StateManager Pattern**: Server-side file persistence to `game_state.json`
- **Previous Issue**: `app.storage.general` was client-side browser localStorage
- **Solution**: Implemented `src/core/state_manager.py` with atomic file writes

### Key Components
- **Persistent Data**: Game state survives app restarts via server-side JSON file
- **Serialization**: Handles conversion of Python types (sets → lists, tuples → lists)
- **Auto-save**: State saved after every user action with debouncing
- **Load on Init**: State restored from file when app starts
- **Atomic Writes**: Uses temp file + rename for data integrity

### State Elements
- `clicked_tiles`: Set of clicked (row, col) positions
- `is_game_closed`: Boolean for game status
- `header_text`: Current header message
- `board_iteration`: Tracks board version
- `bingo_patterns`: Winning patterns found
- `today_seed`: Daily seed for board generation

### Key Functions
- `save_state_to_storage()`: Uses StateManager to persist to file
- `load_state_from_storage()`: Creates new StateManager instance and loads from file
- `toggle_tile()`: Updates tile state and triggers async save
- `close_game()`: Closes game and saves state
- `reopen_game()`: Reopens game and saves state

### StateManager Features
- Async operations with proper locking
- Debounced saves (100ms delay) to reduce I/O
- Singleton pattern for global access
- Thread-safe concurrent access
- Corrupted state recovery
- Atomic file writes with temp file pattern
- 96% test coverage

### StateManager API
```python
# Get singleton instance
from src.core.state_manager import get_state_manager
state_manager = get_state_manager()

# Async operations
await state_manager.toggle_tile(row, col)
await state_manager.update_board(board, iteration, seed)
await state_manager.set_game_closed(is_closed)
await state_manager.update_header(text)
await state_manager.update_bingo_patterns(patterns)
await state_manager.reset_board()

# Get current state
state = await state_manager.get_full_state()

# Properties (read-only)
clicked_tiles = state_manager.clicked_tiles  # Returns copy
is_game_closed = state_manager.is_game_closed
board_iteration = state_manager.board_iteration
```

### Implementation Details
- **File Location**: `game_state.json` (gitignored)
- **Initialization**: Uses `@app.on_startup` for async setup
- **Error Handling**: Gracefully handles missing/corrupted files
- **Performance**: Debounced saves prevent excessive I/O
- **Testing**: Full test suite in `tests/test_state_manager.py`
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