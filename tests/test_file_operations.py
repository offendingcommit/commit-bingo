import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, mock_open, patch

# Add the parent directory to sys.path to import from main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# We need to mock the NiceGUI imports and other dependencies before importing main
sys.modules["nicegui"] = MagicMock()
sys.modules["nicegui.ui"] = MagicMock()
sys.modules["fastapi.staticfiles"] = MagicMock()

# Import the function we want to test
from main import check_phrases_file_change


class TestFileOperations(unittest.TestCase):
    def setUp(self):
        # Create mocks and patches
        self.patches = [
            patch("main.last_phrases_mtime", 123456),
            patch("main.phrases", []),
            patch("main.board", []),
            patch("main.board_views", {}),
            patch("main.board_iteration", 1),
            patch("main.generate_board"),
            patch("main.build_board"),
            patch("main.ui.run_javascript"),
        ]

        for p in self.patches:
            p.start()

    def tearDown(self):
        # Clean up patches
        for p in self.patches:
            p.stop()

    @patch("os.path.getmtime")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="PHRASE1\nPHRASE2\nPHRASE3"
    )
    def test_check_phrases_file_change_no_change(self, mock_file, mock_getmtime):
        """Test when phrases.txt has not changed"""
        import main

        # Mock that the file's mtime is the same as last check
        mock_getmtime.return_value = main.last_phrases_mtime

        # Run the function
        check_phrases_file_change()

        # The file should not have been opened
        mock_file.assert_not_called()

        # generate_board should not have been called
        main.generate_board.assert_not_called()

    @patch("os.path.getmtime")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="PHRASE1\nPHRASE2\nPHRASE3"
    )
    def test_check_phrases_file_change_with_change(self, mock_file, mock_getmtime):
        """Test when phrases.txt has changed"""
        import main

        # Mock that the file's mtime is newer
        mock_getmtime.return_value = main.last_phrases_mtime + 1

        # Setup a mock board_views dictionary
        container_mock = MagicMock()
        tile_buttons_mock = {}
        main.board_views = {"home": (container_mock, tile_buttons_mock)}

        # Run the function
        check_phrases_file_change()

        # The file should have been opened
        mock_file.assert_called_once_with("phrases.txt", "r")

        # last_phrases_mtime should be updated
        self.assertEqual(main.last_phrases_mtime, mock_getmtime.return_value)

        # generate_board should have been called with board_iteration
        main.generate_board.assert_called_once_with(main.board_iteration)

        # Container should have been cleared
        container_mock.clear.assert_called_once()

        # build_board should have been called
        main.build_board.assert_called_once()

        # Container should have been updated
        container_mock.update.assert_called_once()

        # JavaScript should have been executed to resize text
        main.ui.run_javascript.assert_called_once()

    @patch("os.path.getmtime")
    def test_check_phrases_file_change_with_error(self, mock_getmtime):
        """Test when there's an error checking the file"""
        import main

        # Mock that checking the file raises an exception
        mock_getmtime.side_effect = FileNotFoundError("File not found")

        # Run the function - it should not raise an exception
        check_phrases_file_change()

        # No other function should have been called
        main.generate_board.assert_not_called()


if __name__ == "__main__":
    unittest.main()
