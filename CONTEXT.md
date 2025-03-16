# BINGO App Context

## State Persistence
- Game state is persisted across app restarts using `app.storage.general`
- Clicked tiles, game status (open/closed), and header text are saved
- Implemented serialization/deserialization for Python types (sets, tuples)
- Key functions (toggle_tile, reset_board, close_game) save state after changes
- App initialization loads state from storage if available

## View Synchronization
- Two main views: root (/) and stream (/stream)
- NiceGUI 2.11+ compatibility implemented (removed ui.broadcast())
- Timer-based synchronization at 0.05 second intervals
- sync_board_state() handles synchronization between views
- Both views reflect same game state, header text, and board visibility

## User Connection Tracking
- Connected users tracked on both root and stream paths
- Connection/disconnection handled properly
- Health endpoint reports active user counts
- UI displays active user count
- Maintains lists of active user sessions

## Mobile UI Improvements
- Control buttons include text alongside icons
- Improved button styling for better touch targets
- Clearer tooltips with descriptive text
- Consistent styling between game states

## Key Functions
- save_state_to_storage() - Serializes game state to app.storage.general
- load_state_from_storage() - Loads and deserializes state from storage
- toggle_tile() - Updates state and uses timer-based sync
- close_game() - Saves state and updates synchronized views
- reopen_game() - Restores state across synchronized views
- home_page() - Includes user tracking functionality
- stream_page() - Includes user tracking functionality
- health() - Reports system status including active users

## Testing
- State persistence tests verify storage functionality
- Synchronization tests ensure consistent views
- NiceGUI 2.11+ compatibility tests
- UI component tests for controls and board
- User tracking tests for connection handling