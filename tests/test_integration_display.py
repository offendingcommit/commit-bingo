import unittest
import time
import multiprocessing
import requests
from unittest.mock import patch
import sys
import os
from pathlib import Path

class TestBoardDisplay(unittest.TestCase):
    """Integration tests to ensure the board actually displays."""
    
    def setUp(self):
        """Set up the test environment."""
        # Make sure we have test phrases
        self.create_test_phrases()
    
    def create_test_phrases(self):
        """Create a test phrases file if it doesn't exist."""
        # Check if phrases.txt exists, create it if not
        phrases_path = Path("phrases.txt")
        if not phrases_path.exists():
            with open(phrases_path, "w") as f:
                for i in range(1, 30):
                    f.write(f"Test Phrase {i}\n")
    
    def test_board_generation(self):
        """Test that the board generates correctly."""
        # Import board generation code
        from src.core.board import generate_board, board
        from src.core.phrases import initialize_phrases
        
        # Initialize phrases and generate a board
        initialize_phrases()
        result = generate_board(42)
        
        # Verify the board was generated correctly
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 5)  # 5 rows
        for row in result:
            self.assertEqual(len(row), 5)  # 5 columns per row
    
    def test_board_view_components(self):
        """Test that the board view components work correctly."""
        # Import necessary modules
        from src.core.board import generate_board, board, clicked_tiles
        from src.core.phrases import initialize_phrases
        from src.ui.board_view import build_board
        from src.config.constants import FREE_SPACE_TEXT
        from nicegui import ui
        
        # Mock the UI components
        with patch('src.ui.board_view.ui') as mock_ui:
            # Create mock objects
            mock_container = unittest.mock.MagicMock()
            mock_element = unittest.mock.MagicMock()
            mock_grid = unittest.mock.MagicMock()
            mock_card = unittest.mock.MagicMock()
            mock_column = unittest.mock.MagicMock()
            mock_row = unittest.mock.MagicMock()
            mock_label = unittest.mock.MagicMock()
            
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
            
            # Initialize phrases and generate a test board
            initialize_phrases()
            board_data = generate_board(42)
            
            # Build the board
            tile_buttons = {}
            on_click_handler = unittest.mock.MagicMock()
            result = build_board(mock_container, board_data, clicked_tiles, tile_buttons, on_click_handler)
            
            # Verify that the board was built correctly
            self.assertEqual(len(tile_buttons), 25)  # 5x5 = 25 cells
            self.assertTrue((2, 2) in clicked_tiles)  # FREE_SPACE should be clicked
            
            # Check that the FREE_SPACE has the correct style
            free_space_found = False
            for (r, c), tile in tile_buttons.items():
                if board_data[r][c].upper() == FREE_SPACE_TEXT:
                    free_space_found = True
                    # Verify that it's marked as clicked
                    self.assertIn((r, c), clicked_tiles)
                    break
            
            self.assertTrue(free_space_found, "FREE_SPACE not found in the board")

if __name__ == "__main__":
    unittest.main()