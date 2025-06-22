"""
Pure unit tests for game logic functions.
Fast, isolated tests with no I/O or UI dependencies.
"""

import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.config.constants import FREE_SPACE_TEXT
from src.core.game_logic import check_winner, generate_board


@pytest.mark.unit
class TestBoardGeneration:
    """Test board generation logic."""
    
    def test_generate_board_creates_5x5_grid(self):
        """Test that generate_board creates a 5x5 grid."""
        phrases = [f"PHRASE_{i}" for i in range(30)]  # More than needed
        
        board = generate_board(1, phrases)
        
        assert len(board) == 5
        for row in board:
            assert len(row) == 5
    
    def test_generate_board_includes_free_space(self):
        """Test that generate_board includes FREE_SPACE_TEXT at center."""
        phrases = [f"PHRASE_{i}" for i in range(30)]
        
        board = generate_board(1, phrases)
        
        # Center should be free space
        assert board[2][2] == FREE_SPACE_TEXT
    
    def test_generate_board_uses_24_phrases(self):
        """Test that exactly 24 phrases are used (25 - 1 free space)."""
        phrases = [f"PHRASE_{i}" for i in range(30)]
        
        board = generate_board(1, phrases)
        
        # Count non-free-space phrases
        phrase_count = sum(
            1 for row in board for phrase in row 
            if phrase != FREE_SPACE_TEXT
        )
        assert phrase_count == 24
    
    def test_generate_board_deterministic_with_seed(self):
        """Test that same seed produces same board."""
        phrases = [f"PHRASE_{i}" for i in range(30)]
        
        board1 = generate_board(42, phrases)
        board2 = generate_board(42, phrases)
        
        assert board1 == board2
    
    def test_generate_board_different_seeds_different_boards(self):
        """Test that different seeds produce different boards."""
        phrases = [f"PHRASE_{i}" for i in range(30)]
        
        board1 = generate_board(1, phrases)
        board2 = generate_board(2, phrases)
        
        # Boards should be different (except free space)
        different_tiles = sum(
            1 for i in range(5) for j in range(5)
            if (i, j) != (2, 2) and board1[i][j] != board2[i][j]
        )
        assert different_tiles > 0


@pytest.mark.unit
class TestWinConditions:
    """Test bingo win condition checking."""
    
    def setup_method(self):
        """Set up test state before each test."""
        # Mock the global state
        import src.core.game_logic as gl
        gl.clicked_tiles = set()
        gl.bingo_patterns = set()
        gl.is_game_closed = False
    
    @patch('src.core.game_logic.ui.notify')
    def test_check_winner_row_win(self, mock_notify):
        """Test row win detection."""
        import src.core.game_logic as gl

        # Click entire first row
        gl.clicked_tiles = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)}
        
        check_winner()
        
        assert "row0" in gl.bingo_patterns
        mock_notify.assert_called_with("BINGO!", color="green", duration=5)
    
    @patch('src.core.game_logic.ui.notify')
    def test_check_winner_column_win(self, mock_notify):
        """Test column win detection."""
        import src.core.game_logic as gl

        # Click entire first column
        gl.clicked_tiles = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)}
        
        check_winner()
        
        assert "col0" in gl.bingo_patterns
        mock_notify.assert_called_with("BINGO!", color="green", duration=5)
    
    @patch('src.core.game_logic.ui.notify')
    def test_check_winner_main_diagonal(self, mock_notify):
        """Test main diagonal win detection."""
        import src.core.game_logic as gl

        # Click main diagonal
        gl.clicked_tiles = {(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)}
        
        check_winner()
        
        assert "diag_main" in gl.bingo_patterns
        mock_notify.assert_called_with("BINGO!", color="green", duration=5)
    
    @patch('src.core.game_logic.ui.notify')
    def test_check_winner_anti_diagonal(self, mock_notify):
        """Test anti-diagonal win detection."""
        import src.core.game_logic as gl

        # Click anti-diagonal
        gl.clicked_tiles = {(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)}
        
        check_winner()
        
        assert "diag_anti" in gl.bingo_patterns
        mock_notify.assert_called_with("BINGO!", color="green", duration=5)
    
    @patch('src.core.game_logic.ui.notify')
    def test_check_winner_four_corners(self, mock_notify):
        """Test four corners win detection."""
        import src.core.game_logic as gl

        # Click four corners
        gl.clicked_tiles = {(0, 0), (0, 4), (4, 0), (4, 4)}
        
        check_winner()
        
        assert "four_corners" in gl.bingo_patterns
        mock_notify.assert_called_with("Four Corners Bingo!", color="blue", duration=5)
    
    @patch('src.core.game_logic.ui.notify')
    def test_check_winner_plus_shape(self, mock_notify):
        """Test plus shape win detection."""
        import src.core.game_logic as gl

        # Click plus shape (center row and column)
        gl.clicked_tiles = {
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),  # Center row
            (0, 2), (1, 2), (3, 2), (4, 2)           # Center column
        }
        
        check_winner()
        
        assert "plus" in gl.bingo_patterns
        mock_notify.assert_called_with("Plus Bingo!", color="blue", duration=5)
    
    @patch('src.core.game_logic.ui.notify')
    def test_check_winner_blackout(self, mock_notify):
        """Test blackout win detection."""
        import src.core.game_logic as gl

        # Click all tiles
        gl.clicked_tiles = {(r, c) for r in range(5) for c in range(5)}
        
        check_winner()
        
        assert "blackout" in gl.bingo_patterns
        # Multiple special patterns may trigger, check that blackout notification was made
        blackout_calls = [call for call in mock_notify.call_args_list 
                         if call[0][0] == "Blackout Bingo!"]
        assert len(blackout_calls) > 0
    
    @patch('src.core.game_logic.ui.notify')
    def test_check_winner_multiple_wins(self, mock_notify):
        """Test detection of multiple simultaneous wins."""
        import src.core.game_logic as gl

        # Click pattern that creates both row and column win
        gl.clicked_tiles = {
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),  # First row
            (1, 0), (2, 0), (3, 0), (4, 0)           # First column
        }
        
        check_winner()
        
        assert "row0" in gl.bingo_patterns
        assert "col0" in gl.bingo_patterns
        mock_notify.assert_called_with("DOUBLE BINGO!", color="green", duration=5)
    
    @patch('src.core.game_logic.ui.notify')
    def test_check_winner_no_duplicate_notifications(self, mock_notify):
        """Test that patterns aren't re-announced."""
        import src.core.game_logic as gl

        # First win
        gl.clicked_tiles = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)}
        check_winner()
        
        # Clear mock calls
        mock_notify.reset_mock()
        
        # Same win again - should not notify
        check_winner()
        
        mock_notify.assert_not_called()


@pytest.mark.unit
class TestStateManagement:
    """Test game state management functions."""
    
    def setup_method(self):
        """Reset game state before each test."""
        import src.core.game_logic as gl
        gl.clicked_tiles = set()
        gl.bingo_patterns = set()
        gl.is_game_closed = False
        gl.board = []
        gl.board_iteration = 1
        gl.today_seed = None
    
    @patch('src.core.game_logic.save_state_to_storage')
    def test_generate_board_sets_globals(self, mock_save):
        """Test that generate_board updates global state."""
        import src.core.game_logic as gl
        
        phrases = [f"PHRASE_{i}" for i in range(30)]
        
        with patch('datetime.date') as mock_date:
            mock_date.today.return_value.strftime.return_value = "20250101"
            
            board = generate_board(42, phrases)
        
        # Check that globals were updated
        assert gl.board == board
        assert gl.today_seed == "20250101.42"
        assert (2, 2) in gl.clicked_tiles  # Free space clicked
    
    def test_board_structure_consistency(self):
        """Test that board structure is always consistent."""
        phrases = [f"PHRASE_{i}" for i in range(30)]
        
        for seed in range(1, 11):  # Test multiple seeds
            board = generate_board(seed, phrases)
            
            # Should always be 5x5
            assert len(board) == 5
            for row in board:
                assert len(row) == 5
            
            # Should always have free space at center
            assert board[2][2] == FREE_SPACE_TEXT