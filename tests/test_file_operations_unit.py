"""
Pure unit tests for file operations utilities.
Fast, isolated tests with mocked file I/O.
"""

import os
from unittest.mock import mock_open, patch

import pytest

from src.utils.file_operations import has_too_many_repeats, read_phrases_file


@pytest.mark.unit
class TestHasTooManyRepeatsInPhrase:
    """Test the has_too_many_repeats function for individual phrases."""
    
    def test_no_repeats(self):
        """Test phrase with all unique words."""
        assert has_too_many_repeats("ONE TWO THREE FOUR") is False
    
    def test_below_threshold(self):
        """Test phrase with repeats below threshold."""
        # "HELLO WORLD HELLO" - 2/3 = 0.67 > 0.5 (default threshold)
        assert has_too_many_repeats("HELLO WORLD HELLO") is False
    
    def test_above_threshold(self):
        """Test phrase with repeats above threshold."""
        # "HELLO HELLO HELLO HELLO" - 1/4 = 0.25 < 0.5 (threshold)
        assert has_too_many_repeats("HELLO HELLO HELLO HELLO") is True
    
    def test_all_same_word(self):
        """Test phrase with all same word."""
        # "SPAM SPAM SPAM SPAM" - 1/4 = 0.25 < 0.5
        assert has_too_many_repeats("SPAM SPAM SPAM SPAM") is True
    
    def test_custom_threshold(self):
        """Test with custom threshold."""
        phrase = "A B A B"  # 2/4 = 0.5
        
        # With threshold 0.6, this should be rejected
        assert has_too_many_repeats(phrase, threshold=0.6) is True
        
        # With threshold 0.4, this should be accepted
        assert has_too_many_repeats(phrase, threshold=0.4) is False
    
    def test_empty_phrase(self):
        """Test empty phrase."""
        assert has_too_many_repeats("") is False
    
    def test_single_word(self):
        """Test single word phrase."""
        # Single word: 1/1 = 1.0 > any reasonable threshold
        assert has_too_many_repeats("HELLO") is False
    
    def test_whitespace_only(self):
        """Test phrase with only whitespace."""
        assert has_too_many_repeats("   ") is False
    
    @patch('logging.debug')
    def test_logging_on_rejection(self, mock_debug):
        """Test that debug logging occurs when phrase is rejected."""
        phrase = "SPAM SPAM SPAM SPAM"  # 1/4 = 0.25 < 0.5
        result = has_too_many_repeats(phrase)
        
        assert result is True
        mock_debug.assert_called_once()
        
        # Check log message contains useful info
        log_msg = mock_debug.call_args[0][0]
        assert "SPAM SPAM SPAM SPAM" in log_msg
        assert "1/4" in log_msg  # unique/total
        assert "0.25" in log_msg  # ratio


@pytest.mark.unit
class TestReadPhrasesFile:
    """Test the read_phrases_file function."""
    
    def test_read_simple_phrases(self):
        """Test reading simple phrases from file."""
        mock_file_content = """phrase one
phrase two
phrase three"""
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.getmtime', return_value=123456):
                phrases = read_phrases_file()
        
        assert phrases == ["PHRASE ONE", "PHRASE TWO", "PHRASE THREE"]
    
    def test_removes_duplicates_preserves_order(self):
        """Test that duplicates are removed while preserving order."""
        mock_file_content = """first phrase
second phrase
first phrase
third phrase
second phrase"""
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.getmtime', return_value=123456):
                phrases = read_phrases_file()
        
        # Should preserve first occurrence order
        assert phrases == ["FIRST PHRASE", "SECOND PHRASE", "THIRD PHRASE"]
    
    def test_filters_repeated_words(self):
        """Test filtering phrases with too many repeated words."""
        mock_file_content = """good phrase here
spam spam spam spam
another good one
repeat repeat repeat word"""
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.getmtime', return_value=123456):
                phrases = read_phrases_file()
        
        # Should filter out phrases with too many repeats
        assert "GOOD PHRASE HERE" in phrases
        assert "ANOTHER GOOD ONE" in phrases
        assert "SPAM SPAM SPAM SPAM" not in phrases
        # "REPEAT REPEAT REPEAT WORD" has 2/4 = 0.5 = threshold, so it should be kept
        assert "REPEAT REPEAT REPEAT WORD" in phrases
    
    def test_handles_empty_lines(self):
        """Test handling of empty lines in file."""
        mock_file_content = """phrase one

phrase two

phrase three"""
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.getmtime', return_value=123456):
                phrases = read_phrases_file()
        
        assert phrases == ["PHRASE ONE", "PHRASE TWO", "PHRASE THREE"]
    
    def test_strips_whitespace(self):
        """Test stripping of leading/trailing whitespace."""
        mock_file_content = """  phrase one  
\tphrase two\t
phrase three   """
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.getmtime', return_value=123456):
                phrases = read_phrases_file()
        
        assert phrases == ["PHRASE ONE", "PHRASE TWO", "PHRASE THREE"]
    
    def test_converts_to_uppercase(self):
        """Test conversion to uppercase."""
        mock_file_content = """Lower Case
MiXeD CaSe
UPPER CASE"""
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.getmtime', return_value=123456):
                phrases = read_phrases_file()
        
        assert all(phrase.isupper() for phrase in phrases)
        assert phrases == ["LOWER CASE", "MIXED CASE", "UPPER CASE"]
    
    def test_empty_file(self):
        """Test reading empty file."""
        mock_file_content = ""
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.getmtime', return_value=123456):
                phrases = read_phrases_file()
        
        assert phrases == []
    
    def test_case_insensitive_duplicate_detection(self):
        """Test that duplicate detection is case insensitive."""
        mock_file_content = """Hello World
HELLO WORLD
hello world
HeLLo WoRLd"""
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.getmtime', return_value=123456):
                phrases = read_phrases_file()
        
        # Should only keep first occurrence (converted to uppercase)
        assert len(phrases) == 1
        assert phrases == ["HELLO WORLD"]
    
    def test_complex_filtering_scenario(self):
        """Test complex scenario with duplicates and repeats."""
        mock_file_content = """unique phrase one
duplicate phrase
repeat repeat repeat
unique phrase two
duplicate phrase
another repeat repeat repeat
good good phrase"""  # 2/3 = 0.67 > 0.5, should pass
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            with patch('os.path.getmtime', return_value=123456):
                phrases = read_phrases_file()
        
        expected = [
            "UNIQUE PHRASE ONE",
            "DUPLICATE PHRASE",  # First occurrence kept
            "UNIQUE PHRASE TWO", 
            "ANOTHER REPEAT REPEAT REPEAT",  # 2/4 = 0.5 = threshold, kept
            "GOOD GOOD PHRASE"   # 2/3 = 0.67 > threshold, kept
        ]
        assert phrases == expected