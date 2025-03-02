import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to import from main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need to mock the NiceGUI imports and other dependencies before importing main
sys.modules['nicegui'] = MagicMock()
sys.modules['nicegui.ui'] = MagicMock()
sys.modules['fastapi.staticfiles'] = MagicMock()

# Now import functions from the main module
from main import get_line_style_for_lines, get_google_font_css, update_tile_styles

class TestUIFunctions(unittest.TestCase):
    def setUp(self):
        # Setup common test data and mocks
        self.patches = [
            patch('main.BOARD_TILE_FONT', 'Inter'),
            patch('main.BOARD_TILE_FONT_WEIGHT', '700'),
            patch('main.BOARD_TILE_FONT_STYLE', 'normal'),
            patch('main.TILE_CLICKED_BG_COLOR', '#100079'),
            patch('main.TILE_CLICKED_TEXT_COLOR', '#1BEFF5'),
            patch('main.TILE_UNCLICKED_BG_COLOR', '#1BEFF5'),
            patch('main.TILE_UNCLICKED_TEXT_COLOR', '#100079'),
            patch('main.FREE_SPACE_TEXT', 'FREE SPACE'),
            patch('main.FREE_SPACE_TEXT_COLOR', '#FF7f33'),
            patch('main.board', [["PHRASE1", "PHRASE2"], ["PHRASE3", "FREE SPACE"]]),
            patch('main.clicked_tiles', {(1, 1)})  # FREE SPACE is clicked
        ]
        
        for p in self.patches:
            p.start()
    
    def tearDown(self):
        # Clean up patches
        for p in self.patches:
            p.stop()
    
    def test_get_line_style_for_lines(self):
        """Test generating style strings based on line count"""
        import main
        default_text_color = "#000000"
        
        # Test style for a single line
        style_1 = get_line_style_for_lines(1, default_text_color)
        self.assertIn("line-height: 1.5em", style_1)
        self.assertIn(f"color: {default_text_color}", style_1)
        self.assertIn(f"font-family: '{main.BOARD_TILE_FONT}'", style_1)
        
        # Test style for two lines
        style_2 = get_line_style_for_lines(2, default_text_color)
        self.assertIn("line-height: 1.2em", style_2)
        
        # Test style for three lines
        style_3 = get_line_style_for_lines(3, default_text_color)
        self.assertIn("line-height: 0.9em", style_3)
        
        # Test style for four or more lines
        style_4 = get_line_style_for_lines(4, default_text_color)
        self.assertIn("line-height: 0.7em", style_4)
        style_5 = get_line_style_for_lines(5, default_text_color)
        self.assertIn("line-height: 0.7em", style_5)
    
    def test_get_google_font_css(self):
        """Test generating CSS for Google fonts"""
        font_name = "Roboto"
        weight = "400"
        style = "normal"
        uniquifier = "test_font"
        
        css = get_google_font_css(font_name, weight, style, uniquifier)
        
        # Check if CSS contains the expected elements
        self.assertIn(f"font-family: \"{font_name}\"", css)
        self.assertIn(f"font-weight: {weight}", css)
        self.assertIn(f"font-style: {style}", css)
        self.assertIn(f".{uniquifier}", css)
    
    @patch('main.ui.run_javascript')
    def test_update_tile_styles(self, mock_run_js):
        """Test updating tile styles based on clicked state"""
        import main
        
        # Create mock tiles
        tile_buttons_dict = {}
        
        # Create a mock for labels and cards
        for r in range(2):
            for c in range(2):
                mock_card = MagicMock()
                mock_label = MagicMock()
                
                # Create a label info dictionary with the required structure
                label_info = {
                    "ref": mock_label,
                    "base_classes": "some-class",
                    "base_style": "some-style"
                }
                
                tile_buttons_dict[(r, c)] = {
                    "card": mock_card,
                    "labels": [label_info]
                }
        
        # Run the update_tile_styles function
        update_tile_styles(tile_buttons_dict)
        
        # Check that styles were applied to all tiles
        for (r, c), tile in tile_buttons_dict.items():
            # The card's style should have been updated
            tile["card"].style.assert_called_once()
            tile["card"].update.assert_called_once()
            
            # Each label should have had its classes and style updated
            for label_info in tile["labels"]:
                label = label_info["ref"]
                label.classes.assert_called_once_with(label_info["base_classes"])
                label.style.assert_called_once()
                label.update.assert_called_once()
            
            # Check that clicked tiles have the clicked style
            if (r, c) in main.clicked_tiles:
                self.assertIn(main.TILE_CLICKED_BG_COLOR, tile["card"].style.call_args[0][0])
            else:
                self.assertIn(main.TILE_UNCLICKED_BG_COLOR, tile["card"].style.call_args[0][0])
        
        # Check that JavaScript was run to resize text
        mock_run_js.assert_called_once()


if __name__ == '__main__':
    unittest.main()