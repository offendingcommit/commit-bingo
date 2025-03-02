import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from src.core.board import generate_board, toggle_tile, reset_board, clicked_tiles

class TestBoard(unittest.TestCase):
    def setUp(self):
        """Set up mock phrases for testing."""
        # Create a temporary phrases.txt file
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(self.temp_file.name, 'w') as f:
            f.write("PHRASE 1\nPHRASE 2\nPHRASE 3\nPHRASE 4\nPHRASE 5\n")
            f.write("PHRASE 6\nPHRASE 7\nPHRASE 8\nPHRASE 9\nPHRASE 10\n")
            f.write("PHRASE 11\nPHRASE 12\nPHRASE 13\nPHRASE 14\nPHRASE 15\n")
            f.write("PHRASE 16\nPHRASE 17\nPHRASE 18\nPHRASE 19\nPHRASE 20\n")
            f.write("PHRASE 21\nPHRASE 22\nPHRASE 23\nPHRASE 24\nPHRASE 25\n")
        
        # Mock the phrases module
        self.phrases_patcher = patch('src.core.phrases.get_phrases')
        self.mock_get_phrases = self.phrases_patcher.start()
        self.mock_get_phrases.return_value = [
            f"PHRASE {i}" for i in range(1, 26)
        ]
        
        # Reset clicked tiles before each test
        clicked_tiles.clear()
    
    def tearDown(self):
        """Clean up after tests."""
        self.phrases_patcher.stop()
        os.unlink(self.temp_file.name)
    
    def test_generate_board(self):
        """Test that a board is generated with the correct structure."""
        # Directly using the returned board rather than the global variable
        # This makes the test more reliable
        board = generate_board(42)
        
        # Board should be a 5x5 grid
        self.assertEqual(len(board), 5)
        for row in board:
            self.assertEqual(len(row), 5)
        
        # The middle cell should be FREE MEAT
        from src.config.constants import FREE_SPACE_TEXT
        self.assertEqual(board[2][2].upper(), FREE_SPACE_TEXT)
        
        # FREE SPACE should be the only clicked tile initially
        self.assertEqual(len(clicked_tiles), 1)
        self.assertIn((2, 2), clicked_tiles)
    
    def test_toggle_tile(self):
        """Test that toggling a tile works correctly."""
        # Initially, only FREE SPACE should be clicked
        from src.core.board import board
        generate_board(42)
        initial_count = len(clicked_tiles)
        
        # Toggle a tile that isn't FREE SPACE
        toggle_tile(0, 0)
        self.assertEqual(len(clicked_tiles), initial_count + 1)
        self.assertIn((0, 0), clicked_tiles)
        
        # Toggle the same tile again (should remove it)
        toggle_tile(0, 0)
        self.assertEqual(len(clicked_tiles), initial_count)
        self.assertNotIn((0, 0), clicked_tiles)
        
        # Toggle FREE SPACE (should do nothing)
        toggle_tile(2, 2)
        self.assertEqual(len(clicked_tiles), initial_count)
        self.assertIn((2, 2), clicked_tiles)
    
    def test_reset_board(self):
        """Test that resetting the board works correctly."""
        # Set up a board with some clicked tiles
        from src.core.board import board
        generate_board(42)
        toggle_tile(0, 0)
        toggle_tile(1, 1)
        self.assertEqual(len(clicked_tiles), 3)  # FREE SPACE + 2 others
        
        # Reset the board
        reset_board()
        
        # Only FREE SPACE should remain clicked
        self.assertEqual(len(clicked_tiles), 1)
        self.assertIn((2, 2), clicked_tiles)
        self.assertNotIn((0, 0), clicked_tiles)
        self.assertNotIn((1, 1), clicked_tiles)

if __name__ == '__main__':
    unittest.main()