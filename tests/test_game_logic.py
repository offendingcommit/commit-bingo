import unittest
import sys
import os
import random
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to import from main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need to mock the NiceGUI imports and other dependencies before importing main
sys.modules['nicegui'] = MagicMock()
sys.modules['nicegui.ui'] = MagicMock()
sys.modules['fastapi.staticfiles'] = MagicMock()

# Now import functions from the main module
from main import generate_board, has_too_many_repeats, check_winner, split_phrase_into_lines

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        # Setup common test data
        # Mock the global variables used in main.py
        self.patches = [
            patch('main.board', []),
            patch('main.today_seed', ''),
            patch('main.clicked_tiles', set()),
            patch('main.phrases', [f"PHRASE{i}" for i in range(1, 30)]),
            patch('main.FREE_SPACE_TEXT', 'FREE SPACE'),
            patch('main.bingo_patterns', set())
        ]
        
        for p in self.patches:
            p.start()
        
    def tearDown(self):
        # Clean up patches
        for p in self.patches:
            p.stop()
    
    def test_generate_board(self):
        """Test that generate_board creates a 5x5 board with the FREE_SPACE in the middle"""
        import main
        
        # Generate a board with a known seed
        generate_board(42)
        
        # Check if board is created with 5 rows
        self.assertEqual(len(main.board), 5)
        
        # Check if each row has 5 columns
        for row in main.board:
            self.assertEqual(len(row), 5)
        
        # Check if FREE_SPACE is in the middle (2,2)
        self.assertEqual(main.board[2][2], 'FREE SPACE')
        
        # Check if the clicked_tiles set has (2,2) for FREE_SPACE
        self.assertIn((2, 2), main.clicked_tiles)
        
        # Check if the seed is set correctly
        expected_seed = f"{main.datetime.date.today().strftime('%Y%m%d')}.42"
        self.assertEqual(main.today_seed, expected_seed)
    
    def test_has_too_many_repeats(self):
        """Test the function for detecting phrases with too many repeated words"""
        # Test with a phrase having no repeats
        self.assertFalse(has_too_many_repeats("ONE TWO THREE FOUR"))
        
        # Test with a phrase having some repeats but below threshold
        self.assertFalse(has_too_many_repeats("ONE TWO ONE THREE FOUR"))
        
        # Test with a phrase having too many repeats (above default 0.5 threshold)
        self.assertTrue(has_too_many_repeats("ONE ONE ONE ONE TWO"))
        
        # Test with a custom threshold
        self.assertFalse(has_too_many_repeats("ONE ONE TWO THREE", threshold=0.3))
        self.assertTrue(has_too_many_repeats("ONE ONE TWO THREE", threshold=0.8))
        
        # Test with an empty phrase
        self.assertFalse(has_too_many_repeats(""))
    
    def test_check_winner_row(self):
        """Test detecting a win with a complete row"""
        import main
        
        # Setup a board with no wins initially
        main.bingo_patterns = set()
        main.clicked_tiles = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)}
        
        # Mock the ui.notify call
        with patch('main.ui.notify') as mock_notify:
            check_winner()
            
            # Check if the bingo pattern was added
            self.assertIn("row0", main.bingo_patterns)
            
            # Check if the notification was shown
            mock_notify.assert_called_once()
            self.assertEqual(mock_notify.call_args[0][0], "BINGO!")
    
    def test_check_winner_column(self):
        """Test detecting a win with a complete column"""
        import main
        
        # Setup a board with no wins initially
        main.bingo_patterns = set()
        main.clicked_tiles = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)}
        
        # Mock the ui.notify call
        with patch('main.ui.notify') as mock_notify:
            check_winner()
            
            # Check if the bingo pattern was added
            self.assertIn("col0", main.bingo_patterns)
            
            # Check if the notification was shown
            mock_notify.assert_called_once()
            self.assertEqual(mock_notify.call_args[0][0], "BINGO!")
    
    def test_check_winner_diagonal(self):
        """Test detecting a win with a diagonal"""
        import main
        
        # Setup a board with no wins initially
        main.bingo_patterns = set()
        main.clicked_tiles = {(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)}
        
        # Mock the ui.notify call
        with patch('main.ui.notify') as mock_notify:
            check_winner()
            
            # Check if the bingo pattern was added
            self.assertIn("diag_main", main.bingo_patterns)
            
            # Check if the notification was shown
            mock_notify.assert_called_once()
            self.assertEqual(mock_notify.call_args[0][0], "BINGO!")
    
    def test_check_winner_anti_diagonal(self):
        """Test detecting a win with an anti-diagonal"""
        import main
        
        # Setup a board with no wins initially
        main.bingo_patterns = set()
        main.clicked_tiles = {(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)}
        
        # Mock the ui.notify call
        with patch('main.ui.notify') as mock_notify:
            check_winner()
            
            # Check if the bingo pattern was added
            self.assertIn("diag_anti", main.bingo_patterns)
            
            # Check if the notification was shown
            mock_notify.assert_called_once()
            self.assertEqual(mock_notify.call_args[0][0], "BINGO!")
    
    def test_check_winner_special_patterns(self):
        """Test detecting special win patterns like blackout, four corners, etc."""
        import main
        
        # Test four corners pattern
        main.bingo_patterns = set()
        main.clicked_tiles = {(0, 0), (0, 4), (4, 0), (4, 4)}
        
        with patch('main.ui.notify') as mock_notify:
            check_winner()
            self.assertIn("four_corners", main.bingo_patterns)
            mock_notify.assert_called_once()
            self.assertEqual(mock_notify.call_args[0][0], "Four Corners Bingo!")
        
        # Test plus pattern
        main.bingo_patterns = set()
        main.clicked_tiles = set()
        for i in range(5):
            main.clicked_tiles.add((2, i))  # Middle row
            main.clicked_tiles.add((i, 2))  # Middle column
        
        with patch('main.ui.notify') as mock_notify:
            check_winner()
            self.assertIn("plus", main.bingo_patterns)
            # The notify may be called multiple times as the clicks also trigger row/col wins
            self.assertIn(mock_notify.call_args_list[-1][0][0], "Plus Bingo!")
    
    def test_check_winner_multiple_wins(self):
        """Test detecting multiple win patterns in a single check"""
        import main
        
        # Setup a board with two potential wins (a row and a column)
        main.bingo_patterns = set()
        main.clicked_tiles = set()
        
        # Add a complete row and a complete column that intersect
        for i in range(5):
            main.clicked_tiles.add((0, i))  # First row
            main.clicked_tiles.add((i, 0))  # First column
        
        # Mock the ui.notify call
        with patch('main.ui.notify') as mock_notify:
            check_winner()
            
            # Check if both bingo patterns were added
            self.assertIn("row0", main.bingo_patterns)
            self.assertIn("col0", main.bingo_patterns)
            
            # The function should call notify with "DOUBLE BINGO!"
            mock_notify.assert_called_once()
            self.assertEqual(mock_notify.call_args[0][0], "DOUBLE BINGO!")
    
    def test_split_phrase_into_lines(self):
        """Test splitting phrases into balanced lines"""
        # Test with a short phrase (3 words or fewer)
        self.assertEqual(split_phrase_into_lines("ONE TWO THREE"), ["ONE", "TWO", "THREE"])
        
        # Test with a longer phrase - the actual implementation may return different line counts
        # based on the word lengths and balancing algorithm
        result = split_phrase_into_lines("ONE TWO THREE FOUR FIVE")
        self.assertLessEqual(len(result), 4)  # Should not exceed 4 lines
        
        # Test forcing a specific number of lines
        result = split_phrase_into_lines("ONE TWO THREE FOUR FIVE SIX", forced_lines=3)
        self.assertEqual(len(result), 3)  # Should be split into 3 lines
        
        # Test very long phrase
        long_phrase = "ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN"
        result = split_phrase_into_lines(long_phrase)
        self.assertLessEqual(len(result), 4)  # Should never return more than 4 lines


if __name__ == '__main__':
    unittest.main()