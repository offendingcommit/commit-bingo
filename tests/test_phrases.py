import unittest
import tempfile
import os
import time
from unittest.mock import patch
from src.core.phrases import has_too_many_repeats, load_phrases, check_phrases_file_change

class TestPhrases(unittest.TestCase):
    def setUp(self):
        # Create a temporary phrases.txt file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file_path = os.path.join(self.temp_dir.name, "phrases.txt")
        
        with open(self.temp_file_path, 'w') as f:
            f.write("FIRST PHRASE\n")
            f.write("SECOND PHRASE\n")
            f.write("THIRD PHRASE\n")
            f.write("DUPLICATE PHRASE\n")
            f.write("DUPLICATE PHRASE\n")  # Duplicate to test deduplication
            f.write("REPETITIVE WORD WORD WORD\n")  # To test repetition filtering
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_has_too_many_repeats(self):
        """Test the function that checks for repetitive words."""
        # Should return False for a phrase with no repeats
        self.assertFalse(has_too_many_repeats("NO REPEATS HERE"))
        
        # Should return False for a phrase with some repeats (below threshold)
        self.assertFalse(has_too_many_repeats("SOME REPEATS SOME"))
        
        # Should return True for a phrase with many repeats
        self.assertTrue(has_too_many_repeats("WORD WORD WORD WORD WORD"))
    
    def test_check_phrases_file_change(self):
        """Test that file changes are detected."""
        # More complete mocking to ensure test isolation
        with patch('src.core.phrases.os.path.getmtime') as mock_getmtime, \
             patch('src.core.phrases.load_phrases') as mock_load_phrases, \
             patch('src.core.phrases.last_phrases_mtime', 100, create=True):
            
            # First check (file hasn't changed)
            mock_getmtime.return_value = 100  # Same as current timestamp
            result = check_phrases_file_change()
            
            # Should not detect a change if the timestamp is the same
            self.assertFalse(result)
            mock_load_phrases.assert_not_called()
            
            # Reset the mock for the next assertion
            mock_load_phrases.reset_mock()
            
            # Second check (file has changed)
            mock_getmtime.return_value = 200  # Different timestamp
            result = check_phrases_file_change()
            
            # Should detect a change and reload phrases
            self.assertTrue(result)
            mock_load_phrases.assert_called_once()

if __name__ == '__main__':
    unittest.main()