# Bingo Project - Task Completion Checklist

## When Completing Any Task

### 1. Code Quality Checks
```bash
# Run formatters first
poetry run black .
poetry run isort .

# Then run linters
poetry run flake8 main.py src/ tests/
poetry run mypy .
```

### 2. Run Tests
```bash
# Run all tests with coverage
poetry run pytest --cov=src --cov-report=term-missing

# If tests fail, fix and re-run
poetry run pytest
```

### 3. Verify Application Runs
```bash
# Start the app and check it loads without errors
poetry run python app.py
# Visit http://localhost:8080
# Ctrl+C to stop after verification
```

### 4. Check for Regressions
- Verify main view functionality
- Check stream view synchronization
- Test board generation
- Confirm tile clicking works
- Ensure state persistence works

### 5. Update Documentation
- Update CLAUDE.md if architecture changes
- Update README.md for new features
- Add docstrings for new functions
- Update type hints

### 6. Git Operations
```bash
# Check what changed
git status
git diff

# Stage changes atomically
git add src/specific_file.py
git add tests/test_specific_file.py

# Commit with conventional format
git commit -m "type(scope): description"
```

## Common Issues to Check

### State Synchronization
- Missing `ui.broadcast()` calls
- Header updates not propagating to stream view
- Game closed state not checked properly
- Disconnected client exceptions not handled

### Testing Issues
- Mocked dependencies not properly configured
- Race conditions in async tests
- Missing edge case coverage
- Integration tests not updated

### Code Style
- Imports not properly sorted
- Line length exceeding 88 chars
- Missing type hints
- Inconsistent string formatting

## Final Verification
Before marking task complete:
1. All tests pass ✓
2. Code formatted and linted ✓
3. Application starts without errors ✓
4. No regressions introduced ✓
5. Documentation updated if needed ✓
6. Changes committed with proper message ✓