# State Persistence Architecture Analysis

## Current Architecture Issues

### 1. Storage Mechanism
- **Current**: Uses `app.storage.general` which is NiceGUI's wrapper around browser localStorage
- **Problem**: This is client-side storage, not server-side. Each browser has its own storage.
- **Impact**: State is not truly persistent across server restarts or shared between users

### 2. Initialization Flow
```python
# Current flow in app.py
if __name__ in {"__main__", "__mp_main__"}:
    init_app()  # Called once at startup
    ui.run()    # Storage only available AFTER this
```
- **Problem**: Storage is initialized by NiceGUI after `ui.run()`, but we try to load state before
- **Impact**: Initial load always fails, state only works after first save

### 3. Hot Reload Behavior
- **Current**: NiceGUI reloads modules but preserves `app` instance
- **Problem**: Global variables in `game_logic.py` are reset but storage reference is lost
- **Impact**: State saved but globals not properly restored

### 4. Concurrency Issues
- **Current**: No locking or transaction mechanism
- **Problem**: Multiple users can trigger saves simultaneously
- **Impact**: Race conditions causing partial state updates

## Architectural Recommendations

### 1. Server-Side Persistence
Instead of relying on client storage, implement server-side persistence:
```python
# Option A: File-based (simple)
import json
from pathlib import Path

STATE_FILE = Path("game_state.json")

def save_state_to_file():
    with STATE_FILE.open('w') as f:
        json.dump(serialize_state(), f)

# Option B: SQLite (robust)
import sqlite3

def save_state_to_db():
    conn = sqlite3.connect('bingo.db')
    # ... save logic
```

### 2. State Manager Pattern
Create a centralized state manager:
```python
class GameStateManager:
    def __init__(self):
        self._state = self._load_initial_state()
        self._lock = asyncio.Lock()
    
    async def update_tile(self, row, col):
        async with self._lock:
            # Thread-safe updates
            self._state['clicked_tiles'].add((row, col))
            await self._persist()
    
    async def _persist(self):
        # Async save to avoid blocking
        pass
```

### 3. Event-Driven Architecture
Use NiceGUI's reactive features properly:
```python
from nicegui import ui

class BingoGame:
    def __init__(self):
        self.clicked_tiles = ui.state(set())  # Reactive state
        self.load_state()
    
    def toggle_tile(self, row, col):
        with self.clicked_tiles:
            if (row, col) in self.clicked_tiles.value:
                self.clicked_tiles.value.remove((row, col))
            else:
                self.clicked_tiles.value.add((row, col))
        self.save_state()  # Auto-save on change
```

### 4. Proper Lifecycle Hooks
```python
from nicegui import app

@app.on_startup
async def startup():
    """Called once when server starts"""
    await load_server_state()

@app.on_shutdown  
async def shutdown():
    """Called when server stops"""
    await save_final_state()

@ui.page('/')
async def main_page():
    """Called for each new connection"""
    await sync_client_with_server_state()
```

## Testing Strategy

### 1. Unit Tests
- Test state serialization/deserialization
- Test concurrent access handling
- Test corruption recovery

### 2. Integration Tests
- Test full save/load cycle
- Test hot reload scenarios
- Test multi-user synchronization

### 3. BDD Tests
- Use pytest-bdd for scenario testing
- Mock NiceGUI components for isolation
- Test real user workflows

## Migration Path

1. **Phase 1**: Add server-side file persistence alongside current client storage
2. **Phase 2**: Refactor to state manager pattern
3. **Phase 3**: Add proper lifecycle management
4. **Phase 4**: Optimize for concurrent access
5. **Phase 5**: Add monitoring and error recovery

## Key Decisions Needed

1. **Storage Backend**: File, SQLite, Redis, or PostgreSQL?
2. **State Scope**: Single global game or per-session games?
3. **Sync Strategy**: Polling, WebSockets, or SSE?
4. **Recovery Policy**: What happens on corruption?
5. **Performance**: How often to persist? Batch updates?