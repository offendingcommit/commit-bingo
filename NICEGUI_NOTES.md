# NiceGUI Documentation Notes

## Version: 2.11.0

## Key Features and APIs

### app.storage
- Built-in persistent storage system
- Available as `app.storage.general` for general-purpose storage
- Automatically persists across app restarts
- Usage:
  ```python
  # Store data
  app.storage.general['key'] = value
  
  # Retrieve data
  value = app.storage.general.get('key', default_value)
  
  # Check if key exists
  if 'key' in app.storage.general:
      # ...
  ```
- Storage is JSON-serializable, must handle conversion of non-JSON types (like sets)

### Client Synchronization
- `ui.timer(interval, callback)`: Runs a function periodically (interval in seconds)
- `app.on_disconnect(function)`: Registers a callback for when client disconnects
- In NiceGUI 2.11+, updates to UI elements are automatically pushed to all clients
- Use timers for periodic synchronization between clients
- For immediate updates across clients, use a smaller timer interval (e.g., 0.05 seconds)

### UI Controls
- Buttons support both text and icons:
  ```python
  ui.button("Text", icon="icon_name", on_click=handler)
  ```
- Mobile-friendly practices:
  - Use larger touch targets (at least 44x44 pixels)
  - Add descriptive text to icons
  - Use responsive classes

## Best Practices

### State Management
1. Store state in app.storage.general for persistence
2. Convert Python-specific types (sets, tuples) to JSON-compatible types:
   - Sets → Lists
   - Tuples → Lists
3. Convert back when loading
4. Handle serialization errors gracefully

### Synchronization Between Views
1. NiceGUI 2.11+ automatically synchronizes UI element updates between clients
2. Use timers for consistent state synchronization
3. For best results, combine:
   - Fast timers (0.05 seconds) for responsive updates
   - Shared state in app.storage for persistence
   - State loading on page initialization

### Error Handling
1. Wrap storage operations in try/except
2. Handle disconnected clients gracefully
3. Log issues with appropriate level (debug vs error)

### Testing
1. Mock app.storage for unit tests
2. Test serialization/deserialization edge cases
3. Simulate app restarts for integration tests

## Documentation References
- Full API Documentation: https://nicegui.io/documentation
- State Management: https://nicegui.io/documentation#app_storage
- Timers and Async: https://nicegui.io/documentation#ui_timer
- Broadcasting: https://nicegui.io/documentation#ui_broadcast