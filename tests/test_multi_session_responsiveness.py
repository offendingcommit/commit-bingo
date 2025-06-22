"""
Tests for multi-session responsiveness when buttons are clicked from multiple root windows.
"""

import asyncio
import json
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core import game_logic
from src.core.state_manager import GameStateManager, get_state_manager


@pytest.mark.integration
@pytest.mark.slow
class TestMultiSessionResponsiveness(unittest.TestCase):
    """Tests for responsiveness across multiple concurrent sessions."""

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
        
        # Reset singleton
        GameStateManager._instance = None

    def tearDown(self):
        """Clean up after tests."""
        # Clean up state file
        if self.state_file.exists():
            self.state_file.unlink()
        
        # Reset singleton
        GameStateManager._instance = None

    def test_concurrent_tile_clicks_from_multiple_sessions(self):
        """Test that concurrent tile clicks from multiple sessions are handled properly."""
        # Setup board
        game_logic.board = [["A1", "A2", "A3", "A4", "A5"],
                            ["B1", "B2", "B3", "B4", "B5"],
                            ["C1", "C2", "FREE SPACE", "C4", "C5"],
                            ["D1", "D2", "D3", "D4", "D5"],
                            ["E1", "E2", "E3", "E4", "E5"]]
        
        # Track clicks from each session
        session_clicks = {
            "session1": [(0, 0), (0, 1), (0, 2)],  # First row tiles
            "session2": [(1, 0), (1, 1), (1, 2)],  # Second row tiles
            "session3": [(2, 0), (2, 1), (2, 3)],  # Third row tiles (skip FREE SPACE)
            "session4": [(3, 0), (3, 1), (3, 2)],  # Fourth row tiles
            "session5": [(4, 0), (4, 1), (4, 2)],  # Fifth row tiles
        }
        
        # Expected total unique clicks
        expected_clicks = set()
        for clicks in session_clicks.values():
            expected_clicks.update(clicks)
        
        # Simulate concurrent clicks using threads
        def simulate_session_clicks(session_id, clicks):
            """Simulate clicks from a single session."""
            for row, col in clicks:
                game_logic.toggle_tile(row, col)
                # Small delay to simulate real user clicks
                time.sleep(0.01)
        
        # Execute concurrent sessions
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for session_id, clicks in session_clicks.items():
                future = executor.submit(simulate_session_clicks, session_id, clicks)
                futures.append(future)
            
            # Wait for all sessions to complete
            for future in futures:
                future.result()
        
        # Wait for any async saves to complete
        time.sleep(0.5)
        
        # Debug: print what we expect vs what we got
        print(f"Expected clicks: {sorted(expected_clicks)}")
        print(f"Actual clicks: {sorted(game_logic.clicked_tiles)}")
        print(f"Expected count: {len(expected_clicks)}, Actual count: {len(game_logic.clicked_tiles)}")
        
        # Verify all clicks were registered
        self.assertEqual(len(game_logic.clicked_tiles), len(expected_clicks))
        for click in expected_clicks:
            self.assertIn(click, game_logic.clicked_tiles)
        
        # Verify state was persisted
        self.assertTrue(self.state_file.exists())
        with open(self.state_file, 'r') as f:
            saved_state = json.load(f)
        
        self.assertEqual(len(saved_state['clicked_tiles']), len(expected_clicks))

    def test_state_consistency_across_sessions(self):
        """Test that state remains consistent when accessed from multiple sessions."""
        # Setup initial state
        game_logic.board = [["A1", "A2", "A3", "A4", "A5"],
                            ["B1", "B2", "B3", "B4", "B5"],
                            ["C1", "C2", "FREE SPACE", "C4", "C5"],
                            ["D1", "D2", "D3", "D4", "D5"],
                            ["E1", "E2", "E3", "E4", "E5"]]
        game_logic.clicked_tiles = {(0, 0), (1, 1), (2, 2)}
        game_logic.save_state_to_storage()
        time.sleep(0.1)
        
        # Track state reads from multiple sessions
        read_results = {}
        read_lock = Lock()
        
        def read_state_from_session(session_id):
            """Simulate reading state from a session."""
            # Create a new GameStateManager instance (simulating different process/thread)
            state_manager = GameStateManager()
            
            # Get state (get_full_state is synchronous)
            state = state_manager.get_full_state()
            
            with read_lock:
                read_results[session_id] = {
                    'clicked_tiles': state['clicked_tiles'].copy(),
                    'board_iteration': state['board_iteration'],
                    'is_game_closed': state['is_game_closed']
                }
        
        # Simulate multiple sessions reading state concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for i in range(10):
                future = executor.submit(read_state_from_session, f"session{i}")
                futures.append(future)
            
            # Wait for all reads to complete
            for future in futures:
                future.result()
        
        # Verify all sessions read the same state
        first_state = read_results["session0"]
        for session_id, state in read_results.items():
            self.assertEqual(state['clicked_tiles'], first_state['clicked_tiles'], 
                           f"Session {session_id} has different clicked_tiles")
            self.assertEqual(state['board_iteration'], first_state['board_iteration'],
                           f"Session {session_id} has different board_iteration")
            self.assertEqual(state['is_game_closed'], first_state['is_game_closed'],
                           f"Session {session_id} has different is_game_closed")

    def test_button_responsiveness_under_load(self):
        """Test that buttons remain responsive when multiple sessions are active."""
        # Setup board
        game_logic.board = [["A1", "A2", "A3", "A4", "A5"],
                            ["B1", "B2", "B3", "B4", "B5"],
                            ["C1", "C2", "FREE SPACE", "C4", "C5"],
                            ["D1", "D2", "D3", "D4", "D5"],
                            ["E1", "E2", "E3", "E4", "E5"]]
        
        # Track response times
        response_times = []
        response_lock = Lock()
        
        def simulate_button_click(session_id, action_type):
            """Simulate a button click and measure response time."""
            start_time = time.time()
            
            if action_type == "toggle_tile":
                # Random tile click
                import random
                row = random.randint(0, 4)
                col = random.randint(0, 4)
                game_logic.toggle_tile(row, col)
            elif action_type == "close_game":
                game_logic.close_game()
            elif action_type == "reopen_game":
                game_logic.reopen_game()
            elif action_type == "new_board":
                # Simulate new board generation
                game_logic.board_iteration += 1
                game_logic.clicked_tiles.clear()
                game_logic.bingo_patterns.clear()
                game_logic.save_state_to_storage()
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            with response_lock:
                response_times.append(response_time)
        
        # Simulate high load with multiple concurrent sessions
        actions = ["toggle_tile", "close_game", "reopen_game", "new_board", "toggle_tile"] * 10
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i, action in enumerate(actions):
                future = executor.submit(simulate_button_click, f"session{i}", action)
                futures.append(future)
            
            # Wait for all actions to complete
            for future in futures:
                future.result()
        
        # Analyze response times
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        
        # Verify responsiveness (should be under 100ms on average, 600ms max)
        # Note: 600ms allows for occasional event loop conflicts in test environment
        self.assertLess(avg_response_time, 100, 
                       f"Average response time {avg_response_time:.2f}ms exceeds 100ms threshold")
        self.assertLess(max_response_time, 600,
                       f"Maximum response time {max_response_time:.2f}ms exceeds 600ms threshold")
        
        print(f"\nResponse time analysis:")
        print(f"  Average: {avg_response_time:.2f}ms")
        print(f"  Maximum: {max_response_time:.2f}ms")
        print(f"  Total operations: {len(response_times)}")

    def test_ui_updates_propagate_to_all_clients(self):
        """Test that UI updates propagate to all connected clients."""
        # This test simulates the view synchronization mechanism
        
        # Mock the board views for multiple clients
        mock_board_views = {
            "home": (MagicMock(), {}),
            "stream": (MagicMock(), {})
        }
        
        # Create a single tile for position (0,0) that all clients will see
        home_tile = {
            "card": MagicMock(),
            "labels": [{"ref": MagicMock(), "base_classes": "some-class"}]
        }
        mock_board_views["home"][1][(0, 0)] = home_tile
        
        # Create a single tile for stream view  
        stream_tile = {
            "card": MagicMock(),
            "labels": [{"ref": MagicMock(), "base_classes": "some-class"}]
        }
        mock_board_views["stream"][1][(0, 0)] = stream_tile
        
        # Setup board
        mock_board = [["A1", "A2", "A3", "A4", "A5"],
                      ["B1", "B2", "B3", "B4", "B5"],
                      ["C1", "C2", "FREE SPACE", "C4", "C5"],
                      ["D1", "D2", "D3", "D4", "D5"],
                      ["E1", "E2", "E3", "E4", "E5"]]
        
        # Patch and test
        with patch('src.core.game_logic.board_views', mock_board_views), \
             patch('src.core.game_logic.board', mock_board), \
             patch('src.core.game_logic.clicked_tiles', set()), \
             patch('src.core.game_logic.ui', MagicMock()):
            
            # Import and toggle a tile
            from src.core.game_logic import toggle_tile
            toggle_tile(0, 0)
            
            # Verify home view tile received updates
            home_tile["card"].style.assert_called()
            home_tile["card"].update.assert_called()
            
            # Verify stream view tile received updates
            stream_tile["card"].style.assert_called()
            stream_tile["card"].update.assert_called()

    def test_rapid_concurrent_state_changes(self):
        """Test system behavior under rapid concurrent state changes."""
        # Setup board
        game_logic.board = [["A1", "A2", "A3", "A4", "A5"],
                            ["B1", "B2", "B3", "B4", "B5"],
                            ["C1", "C2", "FREE SPACE", "C4", "C5"],
                            ["D1", "D2", "D3", "D4", "D5"],
                            ["E1", "E2", "E3", "E4", "E5"]]
        
        # Track successful operations
        successful_ops = []
        ops_lock = Lock()
        
        def rapid_state_changes(session_id, num_operations):
            """Perform rapid state changes from a session."""
            import random
            
            for i in range(num_operations):
                operation = random.choice(["toggle", "close", "reopen"])
                
                try:
                    if operation == "toggle":
                        row = random.randint(0, 4)
                        col = random.randint(0, 4)
                        game_logic.toggle_tile(row, col)
                    elif operation == "close":
                        game_logic.close_game()
                    elif operation == "reopen":
                        game_logic.reopen_game()
                    
                    with ops_lock:
                        successful_ops.append((session_id, operation))
                    
                    # Very short delay to create contention
                    time.sleep(0.001)
                    
                except Exception as e:
                    print(f"Error in {session_id}: {e}")
        
        # Run rapid changes from multiple sessions
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for i in range(10):
                future = executor.submit(rapid_state_changes, f"session{i}", 20)
                futures.append(future)
            
            # Wait for all to complete
            for future in futures:
                future.result()
        
        # Wait for async operations to complete
        time.sleep(0.5)
        
        # Verify system remained stable
        self.assertEqual(len(successful_ops), 200)  # 10 sessions * 20 operations
        
        # Verify final state is consistent
        self.assertTrue(self.state_file.exists())
        
        # Load and verify state integrity
        game_logic.load_state_from_storage()
        self.assertIsInstance(game_logic.clicked_tiles, set)
        self.assertIsInstance(game_logic.bingo_patterns, set)
        self.assertIsInstance(game_logic.is_game_closed, bool)
        
        print(f"\nRapid operations test:")
        print(f"  Total successful operations: {len(successful_ops)}")
        print(f"  Final clicked tiles: {len(game_logic.clicked_tiles)}")
        print(f"  Game closed: {game_logic.is_game_closed}")


class TestAsyncMultiSessionOperations(unittest.TestCase):
    """Tests for async operations across multiple sessions."""
    
    def setUp(self):
        """Set up test environment."""
        self.state_file = Path("game_state.json")
        if self.state_file.exists():
            self.state_file.unlink()
        
        # Reset singleton
        GameStateManager._instance = None
    
    def tearDown(self):
        """Clean up after tests."""
        if self.state_file.exists():
            self.state_file.unlink()
        
        # Reset singleton
        GameStateManager._instance = None
    
    async def test_async_concurrent_tile_toggles(self):
        """Test async concurrent tile toggles from multiple sessions."""
        state_manager = get_state_manager()
        
        # Initialize board
        board = [["A1", "A2", "A3", "A4", "A5"],
                 ["B1", "B2", "B3", "B4", "B5"],
                 ["C1", "C2", "FREE SPACE", "C4", "C5"],
                 ["D1", "D2", "D3", "D4", "D5"],
                 ["E1", "E2", "E3", "E4", "E5"]]
        
        await state_manager.update_board(board, 1, "test-seed")
        
        # Define tiles to toggle from each session
        session_tiles = {
            "session1": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],  # Row 1
            "session2": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],  # Row 2
            "session3": [(2, 0), (2, 1), (2, 3), (2, 4)],          # Row 3 (skip FREE)
            "session4": [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4)],  # Row 4
            "session5": [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],  # Row 5
        }
        
        # Create async tasks for each session
        async def toggle_tiles_for_session(tiles):
            for row, col in tiles:
                await state_manager.toggle_tile(row, col)
                # Small async delay
                await asyncio.sleep(0.001)
        
        # Run all sessions concurrently
        tasks = []
        for session_id, tiles in session_tiles.items():
            task = asyncio.create_task(toggle_tiles_for_session(tiles))
            tasks.append(task)
        
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)
        
        # Force a save to ensure persistence
        await state_manager.save_state(immediate=True)
        await asyncio.sleep(0.1)  # Give time for save to complete
        
        # Get final state (get_full_state is synchronous)
        final_state = state_manager.get_full_state()
        
        # Verify all tiles were toggled
        expected_tiles = set()
        for tiles in session_tiles.values():
            expected_tiles.update(tiles)
        
        self.assertEqual(len(final_state['clicked_tiles']), len(expected_tiles))
        
        # Verify state was persisted
        self.assertTrue(self.state_file.exists())
    
    def test_async_operations_wrapper(self):
        """Wrapper to run async test in sync context."""
        asyncio.run(self.test_async_concurrent_tile_toggles())


if __name__ == '__main__':
    unittest.main()