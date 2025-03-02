import unittest
from src.utils.text_processing import split_phrase_into_lines

class TestTextProcessing(unittest.TestCase):
    def test_short_phrase_split(self):
        """Test that short phrases (3 words or less) are split into one word per line."""
        phrase = "SHORT TEST PHRASE"
        result = split_phrase_into_lines(phrase)
        self.assertEqual(result, ["SHORT", "TEST", "PHRASE"])
        
    def test_medium_phrase_split(self):
        """Test that medium phrases are split into balanced lines."""
        phrase = "THIS IS A LONGER TEST PHRASE"
        result = split_phrase_into_lines(phrase)
        # Should be split into roughly equal length lines
        self.assertTrue(2 <= len(result) <= 3)  # Should be 2 or 3 lines for medium phrases
        
    def test_long_phrase_split(self):
        """Test that long phrases can be split into multiple lines."""
        phrase = "THIS IS A VERY LONG TEST PHRASE THAT SHOULD BE SPLIT INTO MULTIPLE LINES"
        result = split_phrase_into_lines(phrase)
        # Should have multiple lines
        self.assertTrue(2 <= len(result) <= 4)  # Between 2 and 4 lines
        
    def test_forced_line_count(self):
        """Test forcing a specific number of lines."""
        phrase = "THIS PHRASE SHOULD BE SPLIT INTO EXACTLY THREE LINES"
        result = split_phrase_into_lines(phrase, forced_lines=3)
        self.assertEqual(len(result), 3)

if __name__ == '__main__':
    unittest.main()