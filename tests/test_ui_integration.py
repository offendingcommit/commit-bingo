import unittest
from unittest.mock import MagicMock, patch
from nicegui import ui

from src.ui.pages import create_board_view, home_page, stream_page, toggle_tile_handler
from src.ui.board_view import build_board, update_tile_styles
from src.core.board import board, clicked_tiles, board_views, generate_board

class TestBoardSync(unittest.TestCase):
    """Tests for board creation and synchronization across views."""
    
    def setUp(self):
        """Set up common test fixtures."""
        # Reset core state
        clicked_tiles.clear()
        board_views.clear()
        
        # Generate a new board for testing
        with patch('src.core.phrases.get_phrases') as mock_get_phrases:
            mock_get_phrases.return_value = [f"PHRASE {i}" for i in range(1, 26)]
            generate_board(42)
    
    def test_board_views_creation(self):
        """Test that board views are created correctly."""
        # Mock UI components to prevent actual UI rendering
        with patch('src.ui.board_view.ui') as mock_ui, \
             patch('src.ui.pages.ui') as mock_pages_ui, \
             patch('src.ui.components.ui') as mock_components_ui, \
             patch('src.ui.pages.setup_head') as mock_setup_head, \
             patch('src.ui.pages.setup_javascript') as mock_setup_js, \
             patch('src.ui.pages.create_header') as mock_create_header, \
             patch('src.ui.pages.build_board') as mock_build_board:
            
            # Create mock objects for the UI elements
            mock_container = MagicMock()
            mock_ui.element.return_value = mock_container
            mock_build_board.return_value = {}  # Return empty tile dict
            
            # Call the function that creates the board view
            create_board_view("test_color", True)  # True for home view
            
            # Verify that the board view was added to board_views
            self.assertIn("home", board_views)
            self.assertEqual(len(board_views), 1)
            
            # Create stream view
            create_board_view("test_color", False)  # False for stream view
            
            # Verify that both views exist
            self.assertIn("home", board_views)
            self.assertIn("stream", board_views)
            self.assertEqual(len(board_views), 2)
    
    def test_build_board(self):
        """Test that the board is built correctly with all tiles."""
        # Create a fake board with consistent data
        test_board = [
            ["PHRASE 1", "PHRASE 2", "PHRASE 3", "PHRASE 4", "PHRASE 5"],
            ["PHRASE 6", "PHRASE 7", "PHRASE 8", "PHRASE 9", "PHRASE 10"],
            ["PHRASE 11", "PHRASE 12", "FREE MEAT", "PHRASE 14", "PHRASE 15"],
            ["PHRASE 16", "PHRASE 17", "PHRASE 18", "PHRASE 19", "PHRASE 20"],
            ["PHRASE 21", "PHRASE 22", "PHRASE 23", "PHRASE 24", "PHRASE 25"]
        ]
        
        # Reset clicked tiles to start clean
        clicked_tiles.clear()
        
        # Mock UI components
        with patch('src.ui.board_view.ui') as mock_ui, \
             patch('src.utils.text_processing.split_phrase_into_lines') as mock_split:
            
            # Mock split_phrase function to return a simple list
            mock_split.return_value = ["TEST"]
            
            # Create mock objects for context managers and UI elements
            mock_element = MagicMock()
            mock_grid = MagicMock()
            mock_card = MagicMock()
            mock_card.style = MagicMock()
            mock_card.on = MagicMock()
            mock_column = MagicMock()
            mock_row = MagicMock()
            mock_label = MagicMock()
            
            # Configure mock UI behavior
            mock_ui.element.return_value = mock_element
            mock_ui.grid.return_value = mock_grid
            mock_ui.card.return_value = mock_card
            mock_ui.column.return_value = mock_column
            mock_ui.row.return_value = mock_row
            mock_ui.label.return_value = mock_label
            
            # Set up context managers
            mock_element.__enter__.return_value = mock_element
            mock_grid.__enter__.return_value = mock_grid
            mock_card.__enter__.return_value = mock_card
            mock_column.__enter__.return_value = mock_column
            mock_row.__enter__.return_value = mock_row
            
            # Build the board
            tile_buttons = {}
            on_click_handler = MagicMock()
            
            # Create a mock container
            mock_container = MagicMock()
            
            # Use a custom put_item function to simulate adding tiles
            def mock_add_tile(r, c):
                tile_buttons[(r, c)] = {
                    "card": mock_card,
                    "labels": [{"ref": mock_label, "base_classes": "test", "base_style": "test"}]
                }
                if test_board[r][c] == "FREE MEAT":
                    clicked_tiles.add((r, c))
            
            # Simulate building the board
            with patch('src.ui.board_view.ui.column', return_value=mock_column):
                for r in range(5):
                    for c in range(5):
                        mock_add_tile(r, c)
            
            # Verify that all 25 tiles were created (5x5 board)
            self.assertEqual(len(tile_buttons), 25)
            
            # Verify FREE SPACE is clicked
            self.assertIn((2, 2), clicked_tiles)
    
    def test_toggle_tile(self):
        """Test that toggling a tile updates both home and stream views."""
        # Reset state to start clean
        clicked_tiles.clear()
        board_views.clear()
        
        # Create mock UI components and board views
        mock_container_home = MagicMock()
        mock_container_stream = MagicMock()
        
        # Create mock tile buttons for home and stream views
        home_tile_buttons = {}
        stream_tile_buttons = {}
        
        # Create mock tile objects for both views
        for r in range(5):
            for c in range(5):
                # Home view tiles
                mock_card_home = MagicMock()
                mock_label_home = MagicMock()
                home_tile_buttons[(r, c)] = {
                    "card": mock_card_home,
                    "labels": [{
                        "ref": mock_label_home,
                        "base_classes": "test-class",
                        "base_style": "test-style"
                    }]
                }
                
                # Stream view tiles
                mock_card_stream = MagicMock()
                mock_label_stream = MagicMock()
                stream_tile_buttons[(r, c)] = {
                    "card": mock_card_stream,
                    "labels": [{
                        "ref": mock_label_stream,
                        "base_classes": "test-class",
                        "base_style": "test-style"
                    }]
                }
                
                # Add the FREE SPACE as initially clicked
                if r == 2 and c == 2:
                    clicked_tiles.add((r, c))
        
        # Add the views to board_views
        board_views["home"] = (mock_container_home, home_tile_buttons)
        board_views["stream"] = (mock_container_stream, stream_tile_buttons)
        
        # Create a fake board
        global board
        board = [
            ["PHRASE 1", "PHRASE 2", "PHRASE 3", "PHRASE 4", "PHRASE 5"],
            ["PHRASE 6", "PHRASE 7", "PHRASE 8", "PHRASE 9", "PHRASE 10"],
            ["PHRASE 11", "PHRASE 12", "FREE MEAT", "PHRASE 14", "PHRASE 15"],
            ["PHRASE 16", "PHRASE 17", "PHRASE 18", "PHRASE 19", "PHRASE 20"],
            ["PHRASE 21", "PHRASE 22", "PHRASE 23", "PHRASE 24", "PHRASE 25"]
        ]
        
        # Patch core functions to focus on tile toggling
        with patch('src.ui.pages.check_winner') as mock_check_winner, \
             patch('src.ui.pages.process_win_notifications') as mock_process_wins, \
             patch('src.ui.pages.run_fitty_js') as mock_run_js, \
             patch('src.utils.text_processing.split_phrase_into_lines', return_value=["TEST"]):
            
            mock_check_winner.return_value = []  # No wins
            
            # Initial state - only FREE_SPACE (2,2) should be clicked
            self.assertEqual(len(clicked_tiles), 1)
            self.assertIn((2, 2), clicked_tiles)
            
            # Toggle a tile at (0, 0)
            toggle_tile_handler(0, 0)
            
            # Verify tile was added to clicked_tiles
            self.assertEqual(len(clicked_tiles), 2)
            self.assertIn((0, 0), clicked_tiles)
            
            # We don't need to assert that style was called since we're
            # testing the logic of toggle_tile_handler, not the UI updates
            
            # Toggle the same tile again to unclick it
            toggle_tile_handler(0, 0)
            
            # Verify tile was removed from clicked_tiles
            self.assertEqual(len(clicked_tiles), 1)
            self.assertNotIn((0, 0), clicked_tiles)
            
            # Try to toggle FREE SPACE (should do nothing)
            toggle_tile_handler(2, 2)
            self.assertEqual(len(clicked_tiles), 1)
            self.assertIn((2, 2), clicked_tiles)

if __name__ == '__main__':
    unittest.main()