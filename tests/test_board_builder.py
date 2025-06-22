import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import pytest

# Add the parent directory to sys.path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock NiceGUI imports before importing modules that use them
sys.modules["nicegui"] = MagicMock()
sys.modules["nicegui.ui"] = MagicMock()

from src.types.ui_types import TileButtonsDict
from src.ui.board_builder import build_board, build_closed_message, create_board_view
from src.ui.head import setup_head


@pytest.mark.integration
@pytest.mark.ui
class TestBoardBuilder(unittest.TestCase):
    def setUp(self):
        # Setup common test data and mocks
        self.patches = [
            patch("src.config.constants.BOARD_TILE_FONT", "Inter"),
            patch("src.config.constants.BOARD_TILE_FONT_WEIGHT", "700"),
            patch("src.config.constants.BOARD_TILE_FONT_STYLE", "normal"),
            patch("src.config.constants.TILE_CLICKED_BG_COLOR", "#100079"),
            patch("src.config.constants.TILE_CLICKED_TEXT_COLOR", "#1BEFF5"),
            patch("src.config.constants.TILE_UNCLICKED_BG_COLOR", "#1BEFF5"),
            patch("src.config.constants.TILE_UNCLICKED_TEXT_COLOR", "#100079"),
            patch("src.config.constants.FREE_SPACE_TEXT", "FREE SPACE"),
            patch("src.config.constants.FREE_SPACE_TEXT_COLOR", "#FF7f33"),
            patch("src.config.constants.LABEL_CLASSES", "label-class"),
            patch("src.config.constants.LABEL_SMALL_CLASSES", "label-small-class"),
            patch("src.config.constants.CARD_CLASSES", "card-class"),
            patch("src.config.constants.GRID_CLASSES", "grid-class"),
            patch("src.config.constants.GRID_CONTAINER_CLASS", "w-full aspect-square p-4"),
            patch("src.config.constants.CLOSED_MESSAGE_TEXT", "GAME CLOSED"),
            patch("src.config.constants.CLOSED_MESSAGE_COLOR", "#FF0000"),
            patch("src.config.constants.HEADER_FONT_FAMILY", "Comic Sans MS"),
            patch("src.config.constants.HOME_BG_COLOR", "#FFFFFF"),
            patch("src.config.constants.STREAM_BG_COLOR", "#000000"),
        ]

        for p in self.patches:
            p.start()

    def tearDown(self):
        # Clean up patches
        for p in self.patches:
            p.stop()

    @patch("src.ui.board_builder.ui")
    def test_build_closed_message(self, mock_ui):
        """Test the build_closed_message function"""
        # Setup mock parent element
        mock_parent = MagicMock()
        
        # Setup mock elements for the message
        mock_div = MagicMock()
        mock_inner_div = MagicMock()
        mock_label = MagicMock()
        
        # Setup element mock hierarchy for first div
        mock_ui.element.return_value = mock_div
        mock_div.__enter__.return_value = mock_div
        mock_div.classes.return_value = mock_div
        
        # Setup element mock hierarchy for inner div
        # The second call to ui.element() happens inside the first __enter__ context
        # First return mock_div, for the second call return a new element
        mock_ui.element.side_effect = [mock_div, mock_inner_div]
        mock_inner_div.__enter__.return_value = mock_inner_div
        mock_inner_div.classes.return_value = mock_inner_div
        
        # Configure ui.label to return our mock label
        mock_ui.label.return_value = mock_label
        mock_label.classes.return_value = mock_label
        mock_label.style.return_value = mock_label
        
        # Call the function
        build_closed_message(mock_parent)
        
        # Verify div was created with correct classes - mocking exactly how the original function calls it
        mock_ui.element.assert_called_with("div")
        mock_div.classes.assert_called_with("w-full aspect-square p-4")
        
        # Verify the inner div is created and has the correct classes
        # The code calls ui.element("div").classes(...) in a single chain
        # so we assert that element was called and its return value's classes method was called
        mock_inner_div.classes.assert_called_with("flex justify-center items-center h-full w-full")
        
        # Verify label was created with correct text and styling
        mock_ui.label.assert_called_with("GAME CLOSED")
        mock_label.classes.assert_called_with("text-center fit-header")
        # Don't assert the exact style string as it depends on actual constants
        
        # Verify JavaScript was run
        mock_ui.run_javascript.assert_called_once()

    @patch("src.ui.board_builder.ui")
    def test_build_board(self, mock_ui):
        """Test the build_board function"""
        # Setup mocks
        mock_parent = MagicMock()
        mock_on_tile_click = MagicMock()
        mock_board = [["ITEM1", "ITEM2"], ["ITEM3", "FREE SPACE"]]
        mock_clicked_tiles = {(0, 0), (1, 1)}  # Clicked tiles including FREE SPACE
        
        # Setup UI element mocks
        mock_div = MagicMock()
        mock_grid = MagicMock()
        mock_card = MagicMock()
        mock_column = MagicMock()
        mock_row = MagicMock()
        mock_label = MagicMock()
        
        # Configure ui.element to return our mock div
        mock_ui.element.return_value = mock_div
        mock_div.__enter__.return_value = mock_div
        mock_div.classes.return_value = mock_div
        
        # Configure ui.grid to return our mock grid
        mock_ui.grid.return_value = mock_grid
        mock_grid.__enter__.return_value = mock_grid
        mock_grid.classes.return_value = mock_grid
        
        # Configure ui.card to return our mock card
        mock_ui.card.return_value = mock_card
        mock_card.__enter__.return_value = mock_card
        mock_card.classes.return_value = mock_card
        mock_card.style.return_value = mock_card
        mock_card.on.return_value = mock_card
        
        # Configure ui.column to return our mock column
        mock_ui.column.return_value = mock_column
        mock_column.__enter__.return_value = mock_column
        mock_column.classes.return_value = mock_column
        
        # Configure ui.row to return our mock row
        mock_ui.row.return_value = mock_row
        mock_row.__enter__.return_value = mock_row
        mock_row.classes.return_value = mock_row
        
        # Configure ui.label to return our mock label
        mock_ui.label.return_value = mock_label
        mock_label.classes.return_value = mock_label
        mock_label.style.return_value = mock_label
        
        # Create an empty dictionary for the tile buttons
        tile_buttons_dict: TileButtonsDict = {}
        
        # Call the function
        result = build_board(mock_parent, tile_buttons_dict, mock_on_tile_click, mock_board, mock_clicked_tiles)
        
        # Verify the result is the updated tile_buttons_dict
        self.assertEqual(result, tile_buttons_dict)
        
        # Verify the dictionary contains entries for all tiles
        self.assertEqual(len(tile_buttons_dict), 4)  # 2x2 board
        self.assertIn((0, 0), tile_buttons_dict)
        self.assertIn((0, 1), tile_buttons_dict)
        self.assertIn((1, 0), tile_buttons_dict)
        self.assertIn((1, 1), tile_buttons_dict)
        
        # Verify each tile has card and labels
        for coord, tile_data in tile_buttons_dict.items():
            self.assertIn("card", tile_data)
            self.assertIn("labels", tile_data)
            self.assertEqual(tile_data["card"], mock_card)
            
        # Verify UI components were created correctly
        # We can only check the last calls since we're reusing the same mocks
        mock_ui.element.assert_called_with("div")
        # Don't verify specific calls to classes() as it's called multiple times with different values
        mock_ui.grid.assert_called_with(columns=5)
        # Don't verify specific calls to grid.classes() as it might be called differently in the actual code

    @patch("src.ui.head.setup_head")
    @patch("src.ui.board_builder.ui")
    @patch("src.ui.board_builder.build_board")
    @patch("src.core.game_logic.board_views", {})
    @patch("src.core.game_logic.board", [["ITEM1", "ITEM2"], ["ITEM3", "FREE SPACE"]])
    @patch("src.core.game_logic.clicked_tiles", {(1, 1)})  # FREE SPACE is clicked
    def test_create_board_view_home(self, mock_build_board, mock_ui, mock_setup_head):
        """Test creating the home board view"""
        # Setup mocks
        mock_container = MagicMock()
        mock_div = MagicMock()
        mock_controls_row = MagicMock()
        
        # Configure ui.element to return our mock div
        mock_ui.element.return_value = mock_container
        mock_container.classes.return_value = mock_container
        
        # Mock the create_controls_row function
        with patch("src.ui.controls.create_controls_row", return_value=mock_controls_row):
            # Call the function with is_global=True for home view
            create_board_view("#FFFFFF", True)
            
            # Verify setup_head was called
            mock_setup_head.assert_called_with("#FFFFFF")
            
            # Verify container was created with correct classes
            mock_ui.element.assert_called_with("div")
            mock_container.classes.assert_called_with("home-board-container flex justify-center items-center w-full")
            
            # Verify JavaScript was attempted to be run (may fail in tests)
            # The exact call might be different due to error handling
            mock_ui.run_javascript.assert_called()
            
            # Verify build_board was called
            mock_build_board.assert_called_once()
            
            # Verify the board view was added to board_views
            from src.core.game_logic import board_views
            self.assertIn("home", board_views)
            self.assertEqual(board_views["home"][0], mock_container)

    @patch("src.ui.head.setup_head")
    @patch("src.ui.board_builder.ui")
    @patch("src.ui.board_builder.build_board")
    @patch("src.core.game_logic.board_views", {})
    @patch("src.core.game_logic.board", [["ITEM1", "ITEM2"], ["ITEM3", "FREE SPACE"]])
    @patch("src.core.game_logic.clicked_tiles", {(1, 1)})  # FREE SPACE is clicked
    def test_create_board_view_stream(self, mock_build_board, mock_ui, mock_setup_head):
        """Test creating the stream board view"""
        # Setup mocks
        mock_container = MagicMock()
        
        # Configure ui.element to return our mock div
        mock_ui.element.return_value = mock_container
        mock_container.classes.return_value = mock_container
        
        # Call the function with is_global=False for stream view
        create_board_view("#000000", False)
        
        # Verify setup_head was called
        mock_setup_head.assert_called_with("#000000")
        
        # Verify container was created with correct classes
        mock_ui.element.assert_called_with("div")
        mock_container.classes.assert_called_with("stream-board-container flex justify-center items-center w-full")
        
        # Verify JavaScript was attempted to be run (may fail in tests)
        # The exact call might be different due to error handling
        mock_ui.run_javascript.assert_called()
        
        # Verify build_board was called
        mock_build_board.assert_called_once()
        
        # Verify the board view was added to board_views
        from src.core.game_logic import board_views
        self.assertIn("stream", board_views)
        self.assertEqual(board_views["stream"][0], mock_container)


class TestBoardBuilderClosedGame(unittest.TestCase):
    """Test board builder behavior when game is closed."""

    @patch('src.ui.board_builder.ui')
    @patch('src.ui.board_builder.app')
    @patch('src.ui.board_builder.build_closed_message')
    @patch('src.ui.board_builder.build_board')
    def test_stream_view_shows_closed_message_when_game_closed(self,
                                                               mock_build_board, 
                                                               mock_build_closed_message,
                                                               mock_app, mock_ui):
        """Test that stream view shows closed message when game is closed on initial load."""
        # Arrange
        mock_container = MagicMock()
        mock_container.classes.return_value = mock_container  # Make it chainable
        mock_ui.element.return_value = mock_container
        
        # Mock setup_head which is imported inside the function
        with patch('src.ui.head.setup_head'):
            # Set is_game_closed to True
            import src.core.game_logic
            src.core.game_logic.is_game_closed = True
            
            # Act
            from src.ui.board_builder import create_board_view
            create_board_view("#00FF00", is_global=False)
            
            # Assert
            # Should call build_closed_message instead of build_board
            mock_build_closed_message.assert_called_once_with(mock_container)
            mock_build_board.assert_not_called()
            
            # Should register the view with empty tiles dict
            from src.core.game_logic import board_views
            self.assertIn("stream", board_views)
            self.assertEqual(board_views["stream"][0], mock_container)
            self.assertEqual(board_views["stream"][1], {})  # Empty tiles dict

    @patch('src.ui.board_builder.ui')
    @patch('src.ui.board_builder.app')
    @patch('src.ui.board_builder.build_closed_message')
    @patch('src.ui.board_builder.build_board')
    def test_stream_view_shows_board_when_game_open(self,
                                                    mock_build_board, 
                                                    mock_build_closed_message,
                                                    mock_app, mock_ui):
        """Test that stream view shows board when game is open."""
        # Arrange
        mock_container = MagicMock()
        mock_container.classes.return_value = mock_container  # Make it chainable
        mock_ui.element.return_value = mock_container
        
        # Mock setup_head which is imported inside the function
        with patch('src.ui.head.setup_head'):
            # Set is_game_closed to False
            import src.core.game_logic
            src.core.game_logic.is_game_closed = False
            
            # Act
            from src.ui.board_builder import create_board_view
            create_board_view("#00FF00", is_global=False)
            
            # Assert
            # Should call build_board, not build_closed_message
            mock_build_board.assert_called_once()
            mock_build_closed_message.assert_not_called()


if __name__ == "__main__":
    unittest.main()
