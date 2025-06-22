"""
Tests that reproduce state persistence bugs during app restarts.
These tests are expected to FAIL until we fix the underlying issues.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from nicegui import app, ui

from src.core.game_logic import (
    save_state_to_storage, 
    load_state_from_storage,
    board, clicked_tiles, is_game_closed,
    board_iteration, bingo_patterns, today_seed,
    toggle_tile, generate_board
)
from src.utils.file_operations import read_phrases_file


class TestStatePersistenceBugs:
    """Tests that demonstrate current bugs in state persistence."""
    
    def setup_method(self):
        """Set up test environment."""
        # Reset global state
        global board, clicked_tiles, is_game_closed, board_iteration
        board.clear()
        clicked_tiles.clear()
        is_game_closed = False
        board_iteration = 1
        
        # Mock app.storage.general
        if not hasattr(app, 'storage'):
            app.storage = Mock()
        app.storage.general = {}
    
    def test_state_not_restored_after_hot_reload(self):
        """Test that state is lost when NiceGUI triggers a hot reload."""
        # Arrange: Set up game state
        phrases = read_phrases_file()
        generate_board(1, phrases)
        toggle_tile(0, 0)
        toggle_tile(1, 1)
        assert len(clicked_tiles) == 2
        
        # Save state
        assert save_state_to_storage() is True
        assert 'game_state' in app.storage.general
        
        # Simulate hot reload by clearing globals (what actually happens)
        board.clear()
        clicked_tiles.clear()
        
        # Act: Try to restore state
        restored = load_state_from_storage()
        
        # Assert: This currently FAILS because globals aren't properly restored
        assert restored is True
        assert len(clicked_tiles) == 2  # This will fail!
        assert (0, 0) in clicked_tiles
        assert (1, 1) in clicked_tiles
    
    def test_storage_persistence_across_app_restart(self):
        """Test that storage actually persists when app fully restarts."""
        # Arrange: Save some state
        phrases = read_phrases_file()
        generate_board(1, phrases)
        toggle_tile(2, 2)
        save_state_to_storage()
        
        # Simulate app restart by creating new storage instance
        old_storage = app.storage.general.copy()
        app.storage.general = {}  # This simulates what happens on restart
        
        # Act: Try to load state
        restored = load_state_from_storage()
        
        # Assert: This FAILS because storage is cleared on restart
        assert restored is True  # This will fail!
        assert len(clicked_tiles) == 1
    
    @pytest.mark.asyncio
    async def test_concurrent_state_updates_cause_data_loss(self):
        """Test that concurrent state updates don't cause data loss."""
        # Arrange: Initial state
        phrases = read_phrases_file()
        generate_board(1, phrases)
        
        # Simulate concurrent updates from multiple users
        async def user1_clicks():
            toggle_tile(0, 0)
            await asyncio.sleep(0.01)  # Simulate network delay
            save_state_to_storage()
        
        async def user2_clicks():
            toggle_tile(1, 1)
            await asyncio.sleep(0.01)  # Simulate network delay
            save_state_to_storage()
        
        # Act: Run concurrent updates
        await asyncio.gather(user1_clicks(), user2_clicks())
        
        # Reload state
        clicked_tiles.clear()
        load_state_from_storage()
        
        # Assert: Both clicks should be saved (this may fail due to race condition)
        assert len(clicked_tiles) == 2
        assert (0, 0) in clicked_tiles
        assert (1, 1) in clicked_tiles
    
    def test_state_corruption_on_partial_write(self):
        """Test that partial writes don't corrupt state."""
        # Arrange: Set up state
        phrases = read_phrases_file()
        generate_board(1, phrases)
        toggle_tile(0, 0)
        save_state_to_storage()
        
        # Simulate partial write by corrupting storage
        app.storage.general['game_state']['clicked_tiles'] = "corrupted"
        
        # Act: Try to load corrupted state
        clicked_tiles.clear()
        restored = load_state_from_storage()
        
        # Assert: Should handle corruption gracefully (currently doesn't)
        assert restored is False  # This might fail if error handling is poor
        assert len(clicked_tiles) == 0  # Should be empty after failed load
    
    def test_init_app_called_multiple_times(self):
        """Test that calling init_app multiple times doesn't lose state."""
        from app import init_app
        
        # Arrange: Set up initial state
        phrases = read_phrases_file()
        generate_board(1, phrases)
        toggle_tile(3, 3)
        save_state_to_storage()
        initial_tiles = clicked_tiles.copy()
        
        # Act: Call init_app again (simulates hot reload scenario)
        with patch('app.init_routes'):
            init_app()
        
        # Assert: State should be preserved
        assert clicked_tiles == initial_tiles  # This may fail!


class TestBDDStyleStatePersistence:
    """BDD-style tests for state persistence scenarios."""
    
    def setup_method(self):
        """Given I have a bingo game in progress."""
        # Reset and initialize
        board.clear()
        clicked_tiles.clear()
        is_game_closed = False
        
        if not hasattr(app, 'storage'):
            app.storage = Mock()
        app.storage.general = {}
        
        # Set up game
        phrases = read_phrases_file()
        generate_board(1, phrases)
    
    def test_scenario_graceful_restart(self):
        """
        Scenario: State persists through graceful restart
        """
        # Given I have clicked tiles at positions (0,1), (2,3), and (4,4)
        positions = [(0, 1), (2, 3), (4, 4)]
        for row, col in positions:
            toggle_tile(row, col)
        
        # When the app restarts gracefully
        save_state_to_storage()
        
        # Simulate restart
        clicked_tiles.clear()
        board.clear()
        
        # Then the state should be restored
        assert load_state_from_storage() is True
        
        # And the clicked tiles should remain
        for pos in positions:
            assert pos in clicked_tiles
        
        # And the board should show the same phrases
        assert len(board) == 5
        assert len(board[0]) == 5
    
    def test_scenario_code_change_reload(self):
        """
        Scenario: State persists when code changes trigger reload
        """
        # Given I have a game in progress
        toggle_tile(1, 1)
        toggle_tile(2, 2)
        original_tiles = clicked_tiles.copy()
        
        # When I modify a source file and NiceGUI triggers a hot reload
        save_state_to_storage()
        
        # Simulate what happens during hot reload
        import importlib
        import src.core.game_logic
        
        # Clear module state (simulates reload)
        clicked_tiles.clear()
        board.clear()
        
        # Reload module
        importlib.reload(src.core.game_logic)
        
        # Then the game state should be preserved
        load_state_from_storage()
        assert clicked_tiles == original_tiles  # This likely fails!


def test_nicegui_storage_behavior():
    """Test to understand actual NiceGUI storage behavior."""
    # This test documents the actual behavior we need to work with
    
    # 1. Storage is only available after ui.run() is called
    # 2. Storage uses browser localStorage by default
    # 3. Server restarts clear server-side state
    # 4. Hot reloads may or may not preserve storage
    
    # We need to architect around these constraints
    pass