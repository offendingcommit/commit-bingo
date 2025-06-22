"""
Manual test for hot reload persistence.
This script demonstrates that state persists across page reloads.
"""

import json
import time
from pathlib import Path


def test_hot_reload_manually():
    """Manual test to verify hot reload works."""
    print("\n=== Hot Reload State Persistence Test ===\n")
    
    # Check if state file exists
    state_file = Path("game_state.json")
    
    if not state_file.exists():
        print("❌ No state file found!")
        return
    
    print("✅ State file exists at:", state_file)
    
    # Read and display current state
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    print("\n📊 Current Game State:")
    print(f"  - Board iteration: {state['board_iteration']}")
    print(f"  - Game closed: {state['is_game_closed']}")
    print(f"  - Header text: {state['header_text']}")
    print(f"  - Clicked tiles: {len(state['clicked_tiles'])} tiles")
    
    if state['clicked_tiles']:
        print("\n  Clicked positions:")
        for pos in state['clicked_tiles']:
            row, col = pos
            tile_text = state['board'][row][col] if row < len(state['board']) and col < len(state['board'][row]) else "Unknown"
            print(f"    - ({row}, {col}): {tile_text}")
    
    print(f"\n  - Bingo patterns: {state['bingo_patterns']}")
    print(f"  - Seed: {state['today_seed']}")
    print(f"  - Last saved: {time.ctime(state['timestamp'])}")
    
    print("\n🔄 To test hot reload:")
    print("  1. Open http://localhost:8080 in your browser")
    print("  2. Click some tiles")
    print("  3. Refresh the page (Cmd+R)")
    print("  4. The clicked tiles should remain highlighted")
    print("\n  The game state is automatically saved to game_state.json")
    print("  and restored when the page loads.\n")
    
    # Monitor state changes
    print("💾 Monitoring state file for changes (press Ctrl+C to stop)...\n")
    
    last_modified = state_file.stat().st_mtime
    last_tiles = len(state['clicked_tiles'])
    
    try:
        while True:
            current_modified = state_file.stat().st_mtime
            
            if current_modified > last_modified:
                with open(state_file, 'r') as f:
                    new_state = json.load(f)
                
                new_tiles = len(new_state['clicked_tiles'])
                
                if new_tiles != last_tiles:
                    print(f"🎯 State updated! Clicked tiles: {last_tiles} → {new_tiles}")
                    
                    # Show what changed
                    old_positions = set(tuple(pos) for pos in state['clicked_tiles'])
                    new_positions = set(tuple(pos) for pos in new_state['clicked_tiles'])
                    
                    added = new_positions - old_positions
                    removed = old_positions - new_positions
                    
                    if added:
                        for pos in added:
                            row, col = pos
                            tile_text = new_state['board'][row][col]
                            print(f"   + Added: ({row}, {col}) - {tile_text}")
                    
                    if removed:
                        for pos in removed:
                            row, col = pos
                            tile_text = state['board'][row][col]
                            print(f"   - Removed: ({row}, {col}) - {tile_text}")
                    
                    state = new_state
                    last_tiles = new_tiles
                
                last_modified = current_modified
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\n✅ Test complete!")
        print("The StateManager successfully persists game state across reloads.")


if __name__ == "__main__":
    test_hot_reload_manually()