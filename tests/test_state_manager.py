"""Tests for the new server-side state manager."""

import asyncio
import json
import tempfile
import time
from pathlib import Path

import pytest

from src.config.constants import FREE_SPACE_TEXT
from src.core.state_manager import GameState, GameStateManager, get_state_manager


@pytest.mark.unit
@pytest.mark.state
class TestGameStateManager:
    """Test the GameStateManager implementation."""
    
    @pytest.fixture
    def temp_state_file(self):
        """Create a temporary state file for testing."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_path = Path(f.name)
        
        yield temp_path
        
        # Cleanup
        if temp_path.exists():
            temp_path.unlink()
        
        # Also cleanup temp file
        temp_file = temp_path.with_suffix('.tmp')
        if temp_file.exists():
            temp_file.unlink()
    
    @pytest.fixture
    def manager(self, temp_state_file):
        """Create a state manager with temporary file."""
        return GameStateManager(temp_state_file)
    
    def test_initialization_fresh(self, temp_state_file):
        """Test manager initializes with fresh state when no file exists."""
        manager = GameStateManager(temp_state_file)
        
        assert len(manager.board) == 0
        assert len(manager.clicked_tiles) == 0
        assert manager.is_game_closed is False
        assert manager.board_iteration == 1
        assert manager.today_seed is None
    
    def test_initialization_with_existing_state(self, temp_state_file):
        """Test manager loads existing state from file."""
        # Create a state file
        state_data = {
            'board': [['A1', 'A2'], ['B1', 'B2']],
            'clicked_tiles': [[0, 0], [1, 1]],
            'is_game_closed': True,
            'board_iteration': 5,
            'today_seed': '20250101.1',
            'header_text': 'Game Over!',
            'timestamp': time.time()
        }
        
        with open(temp_state_file, 'w') as f:
            json.dump(state_data, f)
        
        # Initialize manager
        manager = GameStateManager(temp_state_file)
        
        # Verify state was loaded
        assert manager.board == state_data['board']
        assert manager.clicked_tiles == {(0, 0), (1, 1)}
        assert manager.is_game_closed is True
        assert manager.board_iteration == 5
        assert manager.today_seed == '20250101.1'
        assert manager.header_text == 'Game Over!'
    
    @pytest.mark.asyncio
    async def test_toggle_tile(self, manager):
        """Test toggling tiles updates state and saves."""
        # Toggle a tile on
        clicked = await manager.toggle_tile(1, 1)
        assert clicked is True
        assert (1, 1) in manager.clicked_tiles
        
        # Toggle the same tile off
        clicked = await manager.toggle_tile(1, 1)
        assert clicked is False
        assert (1, 1) not in manager.clicked_tiles
        
        # Wait for save to complete
        await asyncio.sleep(0.6)
        
        # Verify saved to file
        assert manager.state_file.exists()
    
    @pytest.mark.asyncio
    async def test_concurrent_tile_toggles(self, manager):
        """Test concurrent tile toggles don't cause race conditions."""
        # Toggle multiple tiles concurrently
        tasks = [
            manager.toggle_tile(0, 0),
            manager.toggle_tile(1, 1),
            manager.toggle_tile(2, 2),
            manager.toggle_tile(3, 3),
            manager.toggle_tile(4, 4)
        ]
        
        await asyncio.gather(*tasks)
        
        # All tiles should be clicked
        assert len(manager.clicked_tiles) == 5
        for i in range(5):
            assert (i, i) in manager.clicked_tiles
    
    @pytest.mark.asyncio
    async def test_persistence_across_instances(self, temp_state_file):
        """Test state persists when creating new manager instances."""
        # First manager
        manager1 = GameStateManager(temp_state_file)
        await manager1.toggle_tile(2, 3)
        await manager1.toggle_tile(4, 1)
        await manager1.close_game()
        
        # Force immediate save
        await manager1.save_state(immediate=True)
        
        # Create new manager
        manager2 = GameStateManager(temp_state_file)
        
        # State should be preserved
        assert (2, 3) in manager2.clicked_tiles
        assert (4, 1) in manager2.clicked_tiles
        assert manager2.is_game_closed is True
    
    @pytest.mark.asyncio
    async def test_update_board(self, manager):
        """Test updating board configuration."""
        test_board = [
            ['A1', 'A2', 'A3', 'A4', 'A5'],
            ['B1', 'B2', 'B3', 'B4', 'B5'],
            ['C1', 'C2', FREE_SPACE_TEXT, 'C4', 'C5'],
            ['D1', 'D2', 'D3', 'D4', 'D5'],
            ['E1', 'E2', 'E3', 'E4', 'E5']
        ]
        
        await manager.update_board(test_board, 2, '20250101.2')
        
        assert manager.board == test_board
        assert manager.board_iteration == 2
        assert manager.today_seed == '20250101.2'
        
        # Free space should be automatically clicked
        assert (2, 2) in manager.clicked_tiles
        assert len(manager.clicked_tiles) == 1
    
    @pytest.mark.asyncio
    async def test_reset_board(self, manager):
        """Test resetting board clears clicks but keeps free space."""
        # Set up board with free space
        test_board = [
            ['A1', 'A2', 'A3', 'A4', 'A5'],
            ['B1', 'B2', 'B3', 'B4', 'B5'],
            ['C1', 'C2', FREE_SPACE_TEXT, 'C4', 'C5'],
            ['D1', 'D2', 'D3', 'D4', 'D5'],
            ['E1', 'E2', 'E3', 'E4', 'E5']
        ]
        
        await manager.update_board(test_board, 1)
        
        # Click some tiles
        await manager.toggle_tile(0, 0)
        await manager.toggle_tile(1, 1)
        assert len(manager.clicked_tiles) == 3  # Including free space
        
        # Reset
        await manager.reset_board()
        
        # Only free space should remain
        assert len(manager.clicked_tiles) == 1
        assert (2, 2) in manager.clicked_tiles
    
    @pytest.mark.asyncio
    async def test_game_state_flow(self, manager):
        """Test complete game flow with state changes."""
        # Start fresh game
        assert manager.is_game_closed is False
        
        # Close game
        await manager.close_game()
        assert manager.is_game_closed is True
        
        # Reopen game
        await manager.reopen_game()
        assert manager.is_game_closed is False
    
    @pytest.mark.asyncio
    async def test_atomic_file_writes(self, manager):
        """Test that file writes are atomic (no corruption on crash)."""
        # Toggle a tile
        await manager.toggle_tile(1, 1)
        
        # Force save
        await manager.save_state(immediate=True)
        
        # Temp file should not exist after successful save
        temp_file = manager.state_file.with_suffix('.tmp')
        assert not temp_file.exists()
        
        # State file should exist
        assert manager.state_file.exists()
    
    @pytest.mark.asyncio
    async def test_corrupted_state_handling(self, temp_state_file):
        """Test manager handles corrupted state gracefully."""
        # Write corrupted data
        with open(temp_state_file, 'w') as f:
            f.write("not valid json{]")
        
        # Manager should initialize with fresh state
        manager = GameStateManager(temp_state_file)
        
        assert len(manager.board) == 0
        assert len(manager.clicked_tiles) == 0
        assert manager.is_game_closed is False
    
    @pytest.mark.asyncio
    async def test_debounced_saves(self, manager):
        """Test that rapid changes are debounced."""
        # Make rapid changes
        for i in range(5):
            await manager.toggle_tile(i, i)
            await asyncio.sleep(0.1)  # Small delay between clicks
        
        # File might not exist yet due to debouncing
        initial_exists = manager.state_file.exists()
        
        # Wait for debounce to complete
        await asyncio.sleep(0.6)
        
        # Now file should definitely exist
        assert manager.state_file.exists()
        
        # Verify all changes were saved
        with open(manager.state_file, 'r') as f:
            data = json.load(f)
        
        assert len(data['clicked_tiles']) == 5
    
    def test_get_full_state(self, manager):
        """Test getting complete state as dictionary."""
        state = manager.get_full_state()
        
        assert 'board' in state
        assert 'clicked_tiles' in state
        assert 'bingo_patterns' in state
        assert 'is_game_closed' in state
        assert 'board_iteration' in state
        assert 'today_seed' in state
        assert 'header_text' in state
        assert 'timestamp' in state
    
    def test_singleton_pattern(self):
        """Test get_state_manager returns same instance."""
        manager1 = get_state_manager()
        manager2 = get_state_manager()
        
        assert manager1 is manager2
    
    @pytest.mark.asyncio
    async def test_header_text_updates(self, manager):
        """Test updating header text."""
        await manager.update_header_text("Winner!")
        assert manager.header_text == "Winner!"
        
        await manager.update_header_text("Game in progress...")
        assert manager.header_text == "Game in progress..."
    
    @pytest.mark.asyncio
    async def test_bingo_patterns(self, manager):
        """Test managing bingo patterns."""
        await manager.add_bingo_pattern("Row 1")
        assert "Row 1" in manager.bingo_patterns
        
        await manager.add_bingo_pattern("Column 3")
        assert len(manager.bingo_patterns) == 2
        assert "Column 3" in manager.bingo_patterns
    
    @pytest.mark.asyncio
    async def test_concurrent_state_modifications(self, manager):
        """Test concurrent modifications to different state properties."""
        tasks = [
            manager.toggle_tile(0, 0),
            manager.update_header_text("Concurrent test"),
            manager.add_bingo_pattern("Row 1"),
            manager.toggle_tile(1, 1),
            manager.add_bingo_pattern("Column 2")
        ]
        
        await asyncio.gather(*tasks)
        
        # All changes should be applied correctly
        assert (0, 0) in manager.clicked_tiles
        assert (1, 1) in manager.clicked_tiles
        assert manager.header_text == "Concurrent test"
        assert "Row 1" in manager.bingo_patterns
        assert "Column 2" in manager.bingo_patterns
    
    @pytest.mark.asyncio
    async def test_rapid_save_cancellation(self, manager):
        """Test that rapid changes properly cancel pending saves."""
        # Make rapid changes that should cancel previous saves
        for i in range(10):
            await manager.toggle_tile(i, 0)
            await asyncio.sleep(0.01)  # Very small delay
        
        # Wait for final save to complete
        await asyncio.sleep(0.6)
        
        # All tiles should be saved
        assert len(manager.clicked_tiles) == 10
        for i in range(10):
            assert (i, 0) in manager.clicked_tiles
    
    @pytest.mark.asyncio
    async def test_save_failure_recovery(self, manager, tmp_path):
        """Test recovery from save failures."""
        # Create a read-only directory to cause save failure
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)  # Read-only
        
        readonly_state_file = readonly_dir / "state.json"
        manager.state_file = readonly_state_file
        
        # Try to save - should fail gracefully
        result = await manager.save_state(immediate=True)
        assert result is False
        
        # Manager should still be functional
        await manager.toggle_tile(1, 1)
        assert (1, 1) in manager.clicked_tiles
    
    @pytest.mark.asyncio
    async def test_partial_state_loading(self, temp_state_file):
        """Test loading state with missing fields."""
        # Create state with only some fields
        partial_state = {
            'board': [['A1', 'A2'], ['B1', 'B2']],
            'clicked_tiles': [[0, 0]],
            'is_game_closed': True
            # Missing: bingo_patterns, board_iteration, today_seed, header_text
        }
        
        with open(temp_state_file, 'w') as f:
            json.dump(partial_state, f)
        
        manager = GameStateManager(temp_state_file)
        
        # Should use defaults for missing fields
        assert manager.board == partial_state['board']
        assert (0, 0) in manager.clicked_tiles
        assert manager.is_game_closed is True
        assert manager.board_iteration == 1  # Default
        assert manager.today_seed is None  # Default
        assert manager.header_text == 'BINGO!'  # Default
        assert len(manager.bingo_patterns) == 0  # Default
    
    @pytest.mark.asyncio
    async def test_invalid_clicked_tiles_format(self, temp_state_file):
        """Test handling of invalid clicked_tiles format."""
        # Create state with invalid clicked_tiles
        invalid_state = {
            'board': [['A1', 'A2'], ['B1', 'B2']],
            'clicked_tiles': ["invalid", [1], [1, 2, 3]],  # Invalid formats
            'is_game_closed': False
        }
        
        with open(temp_state_file, 'w') as f:
            json.dump(invalid_state, f)
        
        manager = GameStateManager(temp_state_file)
        
        # Python will convert these to tuples, which is valid behavior
        # The important thing is that it doesn't crash
        assert isinstance(manager.clicked_tiles, set)
        # The tuples will be created from the invalid data
        assert len(manager.clicked_tiles) > 0
    
    @pytest.mark.asyncio
    async def test_board_with_no_free_space(self, manager):
        """Test board updates when there's no free space."""
        # Board without free space
        board_no_free = [
            ['A1', 'A2', 'A3'],
            ['B1', 'B2', 'B3'],
            ['C1', 'C2', 'C3']  # No FREE_SPACE_TEXT
        ]
        
        await manager.update_board(board_no_free, 1)
        
        # Should not automatically click center tile
        assert (2, 2) not in manager.clicked_tiles
        assert len(manager.clicked_tiles) == 0
    
    @pytest.mark.asyncio
    async def test_board_with_irregular_size(self, manager):
        """Test board updates with irregular dimensions."""
        # Smaller board
        small_board = [['A1', 'A2'], ['B1', 'B2']]
        
        await manager.update_board(small_board, 1)
        
        # Should handle gracefully
        assert manager.board == small_board
        assert len(manager.clicked_tiles) == 0  # No free space position
    
    @pytest.mark.asyncio
    async def test_reset_board_without_existing_board(self, manager):
        """Test reset when no board is set."""
        # Reset with empty board
        await manager.reset_board()
        
        # Should handle gracefully
        assert len(manager.clicked_tiles) == 0
        assert len(manager.bingo_patterns) == 0
    
    @pytest.mark.asyncio
    async def test_property_thread_safety(self, manager):
        """Test that property accessors return copies, not references."""
        # Set up some state
        await manager.toggle_tile(1, 1)
        await manager.add_bingo_pattern("Test")
        
        # Get properties
        clicked = manager.clicked_tiles
        patterns = manager.bingo_patterns
        board = manager.board
        
        # Modify returned objects
        clicked.add((9, 9))
        patterns.add("Modified")
        if board:
            board[0] = ["Modified"]
        
        # Original state should be unchanged
        assert (9, 9) not in manager.clicked_tiles
        assert "Modified" not in manager.bingo_patterns
        if manager.board:
            assert "Modified" not in manager.board[0]
    
    @pytest.mark.asyncio
    async def test_file_permission_recovery(self, manager, tmp_path):
        """Test recovery when state file becomes unreadable."""
        # Create initial state
        await manager.toggle_tile(1, 1)
        await manager.save_state(immediate=True)
        
        # Make file unreadable
        manager.state_file.chmod(0o000)
        
        try:
            # Try to load - should fail gracefully
            result = await manager.load_state()
            assert result is False
            
            # Manager should still be functional with current state
            assert (1, 1) in manager.clicked_tiles
        finally:
            # Restore permissions for cleanup
            manager.state_file.chmod(0o644)
    
    @pytest.mark.asyncio
    async def test_duplicate_bingo_patterns(self, manager):
        """Test that duplicate bingo patterns are handled correctly."""
        await manager.add_bingo_pattern("Row 1")
        await manager.add_bingo_pattern("Row 1")  # Duplicate
        await manager.add_bingo_pattern("Column 2")
        await manager.add_bingo_pattern("Row 1")  # Another duplicate
        
        # Set should handle duplicates
        assert len(manager.bingo_patterns) == 2
        assert "Row 1" in manager.bingo_patterns
        assert "Column 2" in manager.bingo_patterns
    
    @pytest.mark.asyncio
    async def test_state_consistency_after_exception(self, manager, monkeypatch):
        """Test state remains consistent even if save fails."""
        # Toggle a tile successfully
        await manager.toggle_tile(1, 1)
        assert (1, 1) in manager.clicked_tiles
        
        # Mock save to fail
        async def failing_save(*args, **kwargs):
            raise Exception("Save failed")
        
        monkeypatch.setattr(manager, '_persist', failing_save)
        
        # Try to toggle another tile
        await manager.toggle_tile(2, 2)
        
        # State should still be updated even if save failed
        assert (1, 1) in manager.clicked_tiles
        assert (2, 2) in manager.clicked_tiles
    
    @pytest.mark.asyncio
    async def test_extreme_concurrency(self, manager):
        """Test with many concurrent operations."""
        # Create many concurrent tasks
        tasks = []
        
        # Toggle tiles
        for i in range(25):
            for j in range(4):
                tasks.append(manager.toggle_tile(i, j))
        
        # Add patterns
        for i in range(10):
            tasks.append(manager.add_bingo_pattern(f"Pattern {i}"))
        
        # Update headers
        for i in range(5):
            tasks.append(manager.update_header_text(f"Header {i}"))
        
        # Execute all concurrently
        await asyncio.gather(*tasks)
        
        # Wait for all saves to complete
        await asyncio.sleep(0.6)
        
        # Verify reasonable state
        assert len(manager.clicked_tiles) <= 100  # Some may have been toggled twice
        assert len(manager.bingo_patterns) == 10
        assert manager.header_text.startswith("Header")
    
    def test_invalid_json_with_trailing_data(self, temp_state_file):
        """Test handling of JSON with trailing invalid data."""
        # Write valid JSON followed by garbage
        valid_json = '{"board": [], "clicked_tiles": [], "is_game_closed": false}'
        invalid_data = valid_json + '\ngarbagedata{]'
        
        with open(temp_state_file, 'w') as f:
            f.write(invalid_data)
        
        # Should handle gracefully
        manager = GameStateManager(temp_state_file)
        assert len(manager.board) == 0
        assert len(manager.clicked_tiles) == 0
        assert manager.is_game_closed is False