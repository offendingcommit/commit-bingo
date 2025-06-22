"""
Simple multi-session tests that work with the current implementation.
"""

import json
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock
from unittest.mock import patch, MagicMock

from src.core import game_logic


class TestSimpleMultiSession(unittest.TestCase):
    """Simple tests for multi-session scenarios."""

    def setUp(self):
        """Set up test environment."""
        # Clean up any existing state file
        self.state_file = Path("game_state.json")
        if self.state_file.exists():
            self.state_file.unlink()
        
        # Reset game logic state
        game_logic.board = []
        game_logic.clicked_tiles = set()
        game_logic.bingo_patterns = set()
        game_logic.board_iteration = 1
        game_logic.is_game_closed = False
        game_logic.today_seed = None

    def tearDown(self):
        """Clean up after tests."""
        # Clean up state file
        if self.state_file.exists():
            self.state_file.unlink()

    def test_multiple_sessions_clicking_tiles(self):
        """Test multiple sessions clicking different tiles."""
        # Setup board
        game_logic.board = [["A1", "A2", "A3", "A4", "A5"],
                            ["B1", "B2", "B3", "B4", "B5"],
                            ["C1", "C2", "FREE SPACE", "C4", "C5"],
                            ["D1", "D2", "D3", "D4", "D5"],
                            ["E1", "E2", "E3", "E4", "E5"]]
        
        # Session 1 clicks
        game_logic.toggle_tile(0, 0)  # A1
        game_logic.toggle_tile(0, 1)  # A2
        time.sleep(0.1)  # Allow save
        
        # Verify state saved
        self.assertTrue(self.state_file.exists())
        with open(self.state_file, 'r') as f:
            state1 = json.load(f)
        self.assertEqual(len(state1['clicked_tiles']), 2)
        
        # Session 2 loads state and adds more clicks
        game_logic.load_state_from_storage()
        self.assertEqual(len(game_logic.clicked_tiles), 2)
        
        game_logic.toggle_tile(1, 0)  # B1
        game_logic.toggle_tile(1, 1)  # B2
        time.sleep(0.1)  # Allow save
        
        # Verify combined state
        with open(self.state_file, 'r') as f:
            state2 = json.load(f)
        self.assertEqual(len(state2['clicked_tiles']), 4)
        
        # Session 3 loads and verifies all clicks
        game_logic.clicked_tiles.clear()
        game_logic.load_state_from_storage()
        self.assertEqual(len(game_logic.clicked_tiles), 4)
        self.assertIn((0, 0), game_logic.clicked_tiles)
        self.assertIn((0, 1), game_logic.clicked_tiles)
        self.assertIn((1, 0), game_logic.clicked_tiles)
        self.assertIn((1, 1), game_logic.clicked_tiles)

    def test_concurrent_game_state_changes(self):
        """Test concurrent changes to game state."""
        # Setup board
        game_logic.board = [["A1", "A2", "A3", "A4", "A5"],
                            ["B1", "B2", "B3", "B4", "B5"],
                            ["C1", "C2", "FREE SPACE", "C4", "C5"],
                            ["D1", "D2", "D3", "D4", "D5"],
                            ["E1", "E2", "E3", "E4", "E5"]]
        
        results = []
        results_lock = Lock()
        
        def session_action(session_id, action):
            """Perform action and record result."""
            try:
                if action == "close":
                    game_logic.close_game()
                    result = "closed"
                elif action == "reopen":
                    game_logic.reopen_game()
                    result = "reopened"
                elif action == "click":
                    game_logic.toggle_tile(session_id % 5, session_id % 5)
                    result = f"clicked_{session_id % 5}_{session_id % 5}"
                
                with results_lock:
                    results.append((session_id, result))
                    
            except Exception as e:
                with results_lock:
                    results.append((session_id, f"error: {e}"))
        
        # Run concurrent actions
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            actions = ["click", "close", "click", "reopen", "click"]
            for i, action in enumerate(actions):
                future = executor.submit(session_action, i, action)
                futures.append(future)
            
            for future in futures:
                future.result()
        
        # Wait for saves
        time.sleep(0.5)
        
        # Verify results
        self.assertEqual(len(results), 5)
        
        # Load final state
        game_logic.load_state_from_storage()
        
        # Should have some clicked tiles
        self.assertGreater(len(game_logic.clicked_tiles), 0)
        # Final state depends on order of execution
        print(f"Final game closed state: {game_logic.is_game_closed}")
        print(f"Final clicked tiles: {game_logic.clicked_tiles}")

    def test_ui_responsiveness_simulation(self):
        """Simulate UI responsiveness with mocked board views."""
        # Setup board
        game_logic.board = [["A1", "A2", "A3", "A4", "A5"],
                            ["B1", "B2", "B3", "B4", "B5"],
                            ["C1", "C2", "FREE SPACE", "C4", "C5"],
                            ["D1", "D2", "D3", "D4", "D5"],
                            ["E1", "E2", "E3", "E4", "E5"]]
        
        # Mock board views
        mock_board_views = {
            "home": (MagicMock(), {}),
            "stream": (MagicMock(), {})
        }
        
        # Create mock tiles
        for row in range(5):
            for col in range(5):
                for view in ["home", "stream"]:
                    tile = {
                        "card": MagicMock(),
                        "labels": [{"ref": MagicMock(), "base_classes": ""}]
                    }
                    mock_board_views[view][1][(row, col)] = tile
        
        # Test with mocked views
        with patch('src.core.game_logic.board_views', mock_board_views):
            # Click tiles from different "sessions"
            for i in range(3):
                for j in range(3):
                    game_logic.toggle_tile(i, j)
            
            # Verify UI updates were called
            for view in ["home", "stream"]:
                for i in range(3):
                    for j in range(3):
                        tile = mock_board_views[view][1][(i, j)]
                        tile["card"].style.assert_called()
                        tile["card"].update.assert_called()

    def test_state_persistence_across_restarts(self):
        """Test that state persists across simulated restarts."""
        # Initial session - setup and click some tiles
        game_logic.board = [["A1", "A2", "A3", "A4", "A5"],
                            ["B1", "B2", "B3", "B4", "B5"],
                            ["C1", "C2", "FREE SPACE", "C4", "C5"],
                            ["D1", "D2", "D3", "D4", "D5"],
                            ["E1", "E2", "E3", "E4", "E5"]]
        
        # Click a pattern (skip FREE SPACE at 2,2)
        game_logic.toggle_tile(0, 0)
        game_logic.toggle_tile(1, 1)
        game_logic.toggle_tile(3, 3)
        game_logic.toggle_tile(4, 4)
        
        game_logic.is_game_closed = True
        game_logic.save_state_to_storage()
        time.sleep(0.1)
        
        # Simulate restart - clear all state
        game_logic.board = []
        game_logic.clicked_tiles = set()
        game_logic.bingo_patterns = set()
        game_logic.board_iteration = 1
        game_logic.is_game_closed = False
        game_logic.today_seed = None
        
        # Load state after "restart"
        result = game_logic.load_state_from_storage()
        self.assertTrue(result)
        
        # Verify state was restored
        self.assertEqual(len(game_logic.board), 5)
        self.assertEqual(len(game_logic.clicked_tiles), 4)
        self.assertTrue(game_logic.is_game_closed)
        
        # Verify clicked tiles pattern
        self.assertIn((0, 0), game_logic.clicked_tiles)
        self.assertIn((1, 1), game_logic.clicked_tiles)
        self.assertIn((3, 3), game_logic.clicked_tiles)
        self.assertIn((4, 4), game_logic.clicked_tiles)


if __name__ == '__main__':
    unittest.main()