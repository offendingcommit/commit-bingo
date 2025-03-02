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
from main import get_line_style_for_lines, get_google_font_css, update_tile_styles, close_game, sync_board_state, reopen_game, create_board_view

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
        
    @patch('main.ui')
    @patch('main.header_label')
    def test_close_game(self, mock_header_label, mock_ui):
        """Test closing the game functionality"""
        import main
        
        # Mock board views
        mock_container1 = MagicMock()
        mock_container2 = MagicMock()
        mock_buttons1 = {}
        mock_buttons2 = {}
        
        # Set up the board_views global
        main.board_views = {
            "home": (mock_container1, mock_buttons1),
            "stream": (mock_container2, mock_buttons2)
        }
        
        # Mock controls_row
        main.controls_row = MagicMock()
        
        # Ensure is_game_closed is False initially
        main.is_game_closed = False
        
        # Call the close_game function
        main.close_game()
        
        # Verify game is marked as closed
        self.assertTrue(main.is_game_closed)
        
        # Verify header text is updated
        mock_header_label.set_text.assert_called_once_with(main.CLOSED_HEADER_TEXT)
        mock_header_label.update.assert_called_once()
        
        # Verify containers are hidden
        mock_container1.style.assert_called_once_with("display: none;")
        mock_container1.update.assert_called_once()
        mock_container2.style.assert_called_once_with("display: none;")
        mock_container2.update.assert_called_once()
        
        # Verify controls_row is modified (cleared and rebuilt)
        main.controls_row.clear.assert_called_once()
        
        # Verify broadcast is called to update all clients
        mock_ui.broadcast.assert_called_once()
        
        # Verify notification is shown
        mock_ui.notify.assert_called_once_with("Game has been closed", color="red", duration=3)
    
    @patch('main.ui.run_javascript')
    def test_sync_board_state_when_game_closed(self, mock_run_js):
        """Test sync_board_state behavior when game is closed"""
        import main
        
        # Setup mocks
        mock_container1 = MagicMock()
        mock_container2 = MagicMock()
        mock_buttons1 = {}
        mock_buttons2 = {}
        
        # Set up the board_views global
        main.board_views = {
            "home": (mock_container1, mock_buttons1),
            "stream": (mock_container2, mock_buttons2)
        }
        
        # Mock the header label
        main.header_label = MagicMock()
        
        # Mock controls_row with a default_slot attribute
        main.controls_row = MagicMock()
        main.controls_row.default_slot = MagicMock()
        main.controls_row.default_slot.children = []  # Empty initially
        
        # Set game as closed
        main.is_game_closed = True
        
        # Call sync_board_state
        with patch('main.ui') as mock_ui:
            main.sync_board_state()
        
        # Verify header text is updated
        main.header_label.set_text.assert_called_once_with(main.CLOSED_HEADER_TEXT)
        main.header_label.update.assert_called_once()
        
        # Verify containers are hidden
        mock_container1.style.assert_called_once_with("display: none;")
        mock_container1.update.assert_called_once()
        mock_container2.style.assert_called_once_with("display: none;")
        mock_container2.update.assert_called_once()
        
        # Verify controls_row is modified
        main.controls_row.clear.assert_called_once()
        
        # Verify JavaScript was NOT called (should return early for closed games)
        mock_run_js.assert_not_called()
        
    @patch('main.ui')
    def test_header_updates_on_both_paths(self, mock_ui):
        """Test that header gets updated on both root and /stream paths when game state changes"""
        import main
        
        # Mock setup_head function to intercept header creation
        home_header_label = MagicMock()
        stream_header_label = MagicMock()
        
        # We'll track which path is currently being handled
        current_path = None
        
        # Define a side effect for the setup_head function to create different header labels
        # based on which path is being accessed (home or stream)
        def mock_setup_head(background_color):
            nonlocal current_path
            # Set the global header_label based on which path we're on
            if current_path == "home":
                main.header_label = home_header_label
            else:
                main.header_label = stream_header_label
        
        # Create home page board view
        with patch('main.setup_head', side_effect=mock_setup_head), \
             patch('main.build_board') as mock_build_board, \
             patch('main.ui.timer') as mock_timer:
            
            # Create the home page
            current_path = "home"
            mock_home_container = MagicMock()
            mock_ui.element.return_value = mock_home_container
            
            # First, create the home board view
            create_board_view(main.HOME_BG_COLOR, True)
            
            # Create the stream page
            current_path = "stream"
            mock_stream_container = MagicMock()
            mock_ui.element.return_value = mock_stream_container
            
            # Create the stream board view
            create_board_view(main.STREAM_BG_COLOR, False)
            
        # Verify the board views are set up correctly
        self.assertEqual(len(main.board_views), 2)
        self.assertIn("home", main.board_views)
        self.assertIn("stream", main.board_views)
        
        # Reset mocks for the test
        home_header_label.reset_mock()
        stream_header_label.reset_mock()
        mock_home_container.reset_mock()
        mock_stream_container.reset_mock()
        
        # Preserve the original state to restore later
        original_is_game_closed = main.is_game_closed
        
        try:
            # 1. Test Game Closing:
            # Set up for closing the game
            main.is_game_closed = False
            main.header_label = home_header_label  # Start with home page header
            
            # Close the game
            with patch('main.controls_row') as mock_controls_row:
                close_game()
            
            # Verify both headers were updated to show the game is closed
            # First, check the direct update to the current header
            home_header_label.set_text.assert_called_with(main.CLOSED_HEADER_TEXT)
            home_header_label.update.assert_called()
            
            # Reset mocks to test sync
            home_header_label.reset_mock()
            stream_header_label.reset_mock()
            
            # Now, test the sync mechanism ensuring both views reflect the closed state
            
            # Switch to stream header and run sync
            main.header_label = stream_header_label
            sync_board_state()
            
            # Both headers should show closed text (the current one will be directly updated)
            stream_header_label.set_text.assert_called_with(main.CLOSED_HEADER_TEXT)
            stream_header_label.update.assert_called()
            
            # Reset mocks again
            home_header_label.reset_mock()
            stream_header_label.reset_mock()
            
            # 2. Test Game Reopening:
            # Setup for reopening
            with patch('main.reset_board'), \
                 patch('main.generate_board'), \
                 patch('main.build_board'), \
                 patch('main.controls_row'):
                
                # Start with stream header active
                main.header_label = stream_header_label
                
                # Reopen the game
                reopen_game()
                
                # Verify stream header was updated to original text
                stream_header_label.set_text.assert_called_with(main.HEADER_TEXT)
                stream_header_label.update.assert_called()
                
                # Reset mocks
                home_header_label.reset_mock()
                stream_header_label.reset_mock()
                
                # Switch to home header and run sync
                main.header_label = home_header_label
                
                # Simulate that the header might still have the old text
                home_header_label.text = main.CLOSED_HEADER_TEXT
                
                # Since the game is now open, sync should update header text to original
                sync_board_state()
                
                # Header text should be updated to the open game text
                home_header_label.set_text.assert_called_with(main.HEADER_TEXT)
                home_header_label.update.assert_called()
                
        finally:
            # Restore original state
            main.is_game_closed = original_is_game_closed
        
    @patch('main.ui')
    @patch('main.generate_board')
    def test_reopen_game(self, mock_generate_board, mock_ui):
        """Test reopening the game after it has been closed"""
        import main
        
        # Mock board views
        mock_container1 = MagicMock()
        mock_container2 = MagicMock()
        mock_buttons1 = {}
        mock_buttons2 = {}
        
        # Set up the board_views global
        main.board_views = {
            "home": (mock_container1, mock_buttons1),
            "stream": (mock_container2, mock_buttons2)
        }
        
        # Mock header_label
        main.header_label = MagicMock()
        
        # Mock controls_row
        main.controls_row = MagicMock()
        
        # Mock seed_label
        main.seed_label = MagicMock()
        
        # Set initial values
        main.is_game_closed = True
        main.board_iteration = 1
        main.today_seed = "test_seed"
        
        # Call reopen_game
        with patch('main.build_board') as mock_build_board, \
             patch('main.reset_board') as mock_reset_board:
            main.reopen_game()
        
        # Check that the game is no longer closed
        self.assertFalse(main.is_game_closed)
        
        # Verify header text is reset
        main.header_label.set_text.assert_called_once_with(main.HEADER_TEXT)
        main.header_label.update.assert_called_once()
        
        # Verify board_iteration was incremented and generate_board was called
        self.assertEqual(main.board_iteration, 2)  # Incremented from 1
        mock_generate_board.assert_called_once_with(2)
        
        # Verify controls_row was rebuilt
        main.controls_row.clear.assert_called_once()
        
        # Verify containers are shown and rebuilt
        mock_container1.style.assert_called_once_with("display: block;")
        mock_container1.clear.assert_called_once()
        mock_container1.update.assert_called_once()
        mock_container2.style.assert_called_once_with("display: block;")
        mock_container2.clear.assert_called_once()
        mock_container2.update.assert_called_once()
        
        # Verify clicked tiles were reset
        mock_reset_board.assert_called_once()
        
        # Verify notification was shown
        mock_ui.notify.assert_called_once_with("New game started", color="green", duration=3)
        
        # Verify changes were broadcast
        mock_ui.broadcast.assert_called_once()


if __name__ == '__main__':
    unittest.main()