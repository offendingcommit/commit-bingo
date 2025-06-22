"""
Pure unit tests for text processing utilities.
Fast, isolated tests with no dependencies.
"""

import pytest

from src.utils.text_processing import get_line_style_for_lines, split_phrase_into_lines


@pytest.mark.unit
class TestSplitPhraseIntoLines:
    """Test phrase splitting logic."""
    
    def test_single_word_returns_single_line(self):
        """Test that single word phrases return as single line."""
        assert split_phrase_into_lines("Hello") == ["Hello"]
    
    def test_two_words_return_two_lines(self):
        """Test that two word phrases split into two lines."""
        assert split_phrase_into_lines("Hello World") == ["Hello", "World"]
    
    def test_three_words_return_three_lines(self):
        """Test that three word phrases split into three lines."""
        result = split_phrase_into_lines("Hello World Again")
        assert result == ["Hello", "World", "Again"]
    
    def test_four_words_balanced_split(self):
        """Test that four words split into balanced lines."""
        result = split_phrase_into_lines("One Two Three Four")
        assert len(result) == 2
        assert result == ["One Two", "Three Four"]
    
    def test_long_phrase_splits_balanced(self):
        """Test that long phrases split into balanced lines."""
        phrase = "This is a very long phrase that needs splitting"
        result = split_phrase_into_lines(phrase)
        
        # Should split into multiple lines (2-4)
        assert 2 <= len(result) <= 4
        
        # Check that no line is empty
        assert all(line.strip() for line in result)
        
        # Check that all words are preserved
        original_words = phrase.split()
        result_words = " ".join(result).split()
        assert original_words == result_words
    
    def test_forced_lines_parameter(self):
        """Test forcing specific number of lines."""
        phrase = "One Two Three Four Five Six"
        
        # Force 2 lines
        result_2 = split_phrase_into_lines(phrase, forced_lines=2)
        assert len(result_2) == 2
        
        # Force 3 lines
        result_3 = split_phrase_into_lines(phrase, forced_lines=3)
        assert len(result_3) == 3
        
        # Force 4 lines
        result_4 = split_phrase_into_lines(phrase, forced_lines=4)
        assert len(result_4) == 4
    
    def test_forced_lines_with_short_phrase(self):
        """Test forced lines with phrase that has fewer words."""
        phrase = "One Two"
        
        # Can't force more lines than words
        result = split_phrase_into_lines(phrase, forced_lines=3)
        assert len(result) == 2  # Falls back to word count
    
    def test_maximum_four_lines(self):
        """Test that function never returns more than 4 lines."""
        # Very long phrase
        phrase = " ".join([f"Word{i}" for i in range(20)])
        result = split_phrase_into_lines(phrase)
        
        assert len(result) <= 4
    
    def test_empty_phrase(self):
        """Test handling of empty phrase."""
        result = split_phrase_into_lines("")
        assert len(result) == 0  # Returns [] for empty input
    
    def test_phrase_with_extra_spaces(self):
        """Test handling of phrases with multiple spaces."""
        phrase = "One   Two    Three"
        result = split_phrase_into_lines(phrase)
        
        # Should handle extra spaces correctly
        assert len(result) == 3
        assert result == ["One", "Two", "Three"]


@pytest.mark.unit
class TestGetLineStyleForLines:
    """Test line style calculation for different line counts."""
    
    def test_single_line_style(self):
        """Test style for single line."""
        style = get_line_style_for_lines(1, "#000000")
        
        assert "line-height: 1.5em" in style
        assert "font-family:" in style
        assert "font-weight:" in style
        assert "color: #000000" in style
    
    def test_two_line_style(self):
        """Test style for two lines."""
        style = get_line_style_for_lines(2, "#000000")
        
        assert "line-height: 1.2em" in style
        assert "color: #000000" in style
    
    def test_three_line_style(self):
        """Test style for three lines."""
        style = get_line_style_for_lines(3, "#000000")
        
        assert "line-height: 0.9em" in style
        assert "color: #000000" in style
    
    def test_four_line_style(self):
        """Test style for four lines."""
        style = get_line_style_for_lines(4, "#000000")
        
        assert "line-height: 0.7em" in style
        assert "color: #000000" in style
    
    def test_style_includes_font_properties(self):
        """Test that all font properties are included."""
        style = get_line_style_for_lines(1, "#000000")
        
        assert "font-family:" in style
        assert "font-style:" in style
        assert "font-weight:" in style
        assert "line-height:" in style
        assert "color:" in style
    
    def test_different_colors(self):
        """Test that different colors are applied correctly."""
        style_black = get_line_style_for_lines(1, "#000000")
        style_white = get_line_style_for_lines(1, "#ffffff")
        
        assert "color: #000000" in style_black
        assert "color: #ffffff" in style_white