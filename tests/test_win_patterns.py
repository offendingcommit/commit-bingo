import unittest
from src.core.win_patterns import check_winner

class TestWinPatterns(unittest.TestCase):
    def setUp(self):
        """Reset the bingo_patterns set before each test."""
        # Access the module's global variable and reset it
        import src.core.win_patterns
        src.core.win_patterns.bingo_patterns = set()
    
    def test_row_win(self):
        """Test that a complete row is detected as a win."""
        # Create a set with a complete row (row 0)
        clicked_tiles = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)}
        
        # Check for win patterns
        new_patterns = check_winner(clicked_tiles)
        
        # Should detect row0 as a win
        self.assertIn("row0", new_patterns)
        self.assertEqual(len(new_patterns), 1)  # Only one pattern should be detected
    
    def test_column_win(self):
        """Test that a complete column is detected as a win."""
        # Create a set with a complete column (column 2)
        clicked_tiles = {(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)}
        
        # Check for win patterns
        new_patterns = check_winner(clicked_tiles)
        
        # Should detect col2 as a win
        self.assertIn("col2", new_patterns)
        self.assertEqual(len(new_patterns), 1)  # Only one pattern should be detected
    
    def test_diagonal_win(self):
        """Test that complete diagonals are detected as wins."""
        # Create a set with the main diagonal
        clicked_tiles = {(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)}
        
        # Check for win patterns
        new_patterns = check_winner(clicked_tiles)
        
        # Should detect the main diagonal as a win
        self.assertIn("diag_main", new_patterns)
        self.assertEqual(len(new_patterns), 1)  # Only one pattern should be detected
        
        # Reset bingo_patterns
        import src.core.win_patterns
        src.core.win_patterns.bingo_patterns = set()
        
        # Test anti-diagonal
        clicked_tiles = {(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)}
        new_patterns = check_winner(clicked_tiles)
        
        # Should detect the anti-diagonal as a win
        self.assertIn("diag_anti", new_patterns)
        self.assertEqual(len(new_patterns), 1)  # Only one pattern should be detected
    
    def test_special_patterns(self):
        """Test that special patterns are detected correctly."""
        # Test four corners pattern
        clicked_tiles = {(0, 0), (0, 4), (4, 0), (4, 4)}
        
        # Check for win patterns
        new_patterns = check_winner(clicked_tiles)
        
        # Should detect four corners as a win
        self.assertIn("four_corners", new_patterns)
        self.assertEqual(len(new_patterns), 1)  # Only one pattern should be detected

if __name__ == '__main__':
    unittest.main()