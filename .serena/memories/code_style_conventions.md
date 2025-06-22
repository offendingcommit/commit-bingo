# Bingo Project - Code Style & Conventions

## Python Code Style

### General Guidelines
- **Python Version**: 3.12+
- **Line Length**: 88 characters (Black's default)
- **Indentation**: 4 spaces (no tabs)
- **String Formatting**: Use f-strings for interpolation

### Imports
1. Standard library imports first
2. Third-party imports second
3. Local module imports last
4. Each group alphabetically sorted
5. Use `from typing import` for type hints

Example:
```python
import datetime
import logging
import random
from typing import List, Optional, Set, Dict, Any

from nicegui import ui, app

from src.config.constants import HEADER_TEXT
from src.types.ui_types import BoardType
```

### Naming Conventions
- **Functions/Variables**: `snake_case`
- **Constants**: `UPPER_CASE` (defined at top of file)
- **Classes**: `PascalCase`
- **Type Aliases**: `PascalCase`
- **Private Methods**: `_leading_underscore`

### Type Hints
- Use type hints for all function signatures
- Use `Optional[T]` for nullable types
- Use `List`, `Dict`, `Set`, `Tuple` from typing
- Define custom types in `src/types/`

### Documentation
- Triple-quoted docstrings for modules and functions
- Brief description at module level
- No inline comments unless absolutely necessary
- Descriptive variable/function names over comments

### Error Handling
- Use try/except blocks with specific exceptions
- Log errors using the logging module
- Provide meaningful error messages

### NiceGUI Specific
- Define UI element styling as class constants
- Use context managers for UI containers
- Separate UI logic from business logic
- Handle disconnected clients gracefully

### Code Organization
- Keep functions focused and single-purpose
- Extract constants to config module
- Separate concerns into appropriate modules
- Use type definitions for complex data structures

### Testing Conventions
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Use pytest fixtures for setup
- Mock external dependencies
- Aim for high test coverage

## Formatting Tools
- **Black**: Automatic code formatting
- **isort**: Import sorting with Black compatibility
- **flake8**: Linting (configured for 88 char lines)
- **mypy**: Static type checking

All formatting is automated via `make format` or individual Poetry commands.