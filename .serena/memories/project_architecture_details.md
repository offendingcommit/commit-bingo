# Bingo Project - Architecture Details

## Core Architecture Patterns

### State Management
- **Global State**: Maintained in `src/core/game_logic.py`
  - `board`: 2D array of phrases
  - `clicked_tiles`: Set of (row, col) tuples
  - `bingo_patterns`: Set of winning patterns found
  - `board_iteration`: Integer tracking board version
  - `is_game_closed`: Boolean flag
  - `today_seed`: Optional string for daily boards

### Persistence Layer
- Uses NiceGUI's `app.storage.general` for persistence
- Serialization/deserialization for non-JSON types:
  - Sets converted to lists for storage
  - Tuples converted to lists and back
- State saved on every user action
- State loaded on app initialization

### UI Architecture
- **Two Views**: 
  - Root path (`/`) - Full interactive board
  - Stream path (`/stream`) - Read-only view
- **Synchronization**: Timer-based at 0.05s intervals
- **User Tracking**: Active connections per path
- **Health Endpoint**: `/health` returns JSON status

### Module Organization
```
src/
├── config/       # Constants and configuration
├── core/         # Business logic (game_logic.py)
├── ui/           # UI components
│   ├── board_builder.py  # Board rendering
│   ├── controls.py       # Control buttons
│   ├── head.py          # HTML head configuration
│   ├── routes.py        # Route definitions
│   └── sync.py          # View synchronization
├── utils/        # Helpers
│   ├── file_monitor.py   # File watching
│   ├── file_operations.py # File I/O
│   └── text_processing.py # Text manipulation
└── types/        # Type definitions

```

### Key Design Decisions
1. **Separation of Concerns**: UI logic separate from game logic
2. **Type Safety**: Comprehensive type hints throughout
3. **Testability**: Modular design enables unit testing
4. **Backward Compatibility**: Legacy main.py kept but deprecated
5. **Mobile-First**: Touch-friendly UI with text+icon buttons

### Integration Points
- NiceGUI for reactive web UI
- FastAPI (via NiceGUI) for HTTP endpoints
- Poetry for dependency management
- pytest for testing framework
- GitHub Actions for CI/CD

### Performance Considerations
- Timer-based sync minimizes overhead
- State persistence is async-friendly
- Efficient board generation with seeded randomization
- Minimal DOM updates via NiceGUI's reactivity