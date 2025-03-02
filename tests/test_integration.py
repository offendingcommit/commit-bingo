import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path to import from main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# We need to mock the NiceGUI imports and other dependencies before importing main
sys.modules["nicegui"] = MagicMock()
sys.modules["nicegui.ui"] = MagicMock()
sys.modules["fastapi.staticfiles"] = MagicMock()

# This test doesn't import main.py directly, but rather tests the interactions
# between various functions in an integration manner


class TestBingoIntegration(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=unittest.mock.mock_open,
        read_data="PHRASE1\nPHRASE2\nPHRASE3\nPHRASE4\nPHRASE5\nPHRASE6\nPHRASE7\nPHRASE8\nPHRASE9\nPHRASE10\nPHRASE11\nPHRASE12\nPHRASE13\nPHRASE14\nPHRASE15\nPHRASE16\nPHRASE17\nPHRASE18\nPHRASE19\nPHRASE20\nPHRASE21\nPHRASE22\nPHRASE23\nPHRASE24\nPHRASE25\n",
    )
    def test_full_game_flow(self, mock_open):
        """
        Test the full game flow from initializing the board to winning the game
        """
        # Import main here so we can mock the open() call before it reads phrases.txt
        import main

        # Reset global state for testing
        main.board = []
        main.clicked_tiles = set()
        main.bingo_patterns = set()
        main.board_iteration = 1

        # Mock ui functions
        ui_mock = MagicMock()
        main.ui = ui_mock

        # Step 1: Generate a new board with a fixed seed
        main.generate_board(42)

        # Check if board was generated correctly
        self.assertEqual(len(main.board), 5)
        self.assertEqual(
            main.board[2][2], main.FREE_SPACE_TEXT
        )  # Use the actual constant value
        self.assertIn((2, 2), main.clicked_tiles)

        # Step 2: Set up a win scenario by clicking a row
        with patch("main.ui.notify") as mock_notify:
            # Click the remaining tiles in the first row
            for col in range(5):
                if (0, col) not in main.clicked_tiles:
                    main.toggle_tile(0, col)

            # Check if the win was detected
            self.assertIn("row0", main.bingo_patterns)

            # Check if notification was shown
            mock_notify.assert_called_with("BINGO!", color="green", duration=5)

        # Step 3: Reset the board
        main.reset_board()

        # Check if clicked_tiles was reset (except FREE SPACE)
        self.assertEqual(len(main.clicked_tiles), 1)
        self.assertIn((2, 2), main.clicked_tiles)

        # Check if bingo_patterns was cleared
        self.assertEqual(len(main.bingo_patterns), 0)

        # Step 4: Generate a new board
        prev_board = [row[:] for row in main.board]  # Make a deep copy

        main.generate_new_board()

        # Check if a new board was generated
        self.assertEqual(main.board_iteration, 2)

        # Board should have changed in at least some places
        different_elements = 0
        for r in range(5):
            for c in range(5):
                if (r, c) != (2, 2) and main.board[r][c] != prev_board[r][c]:
                    different_elements += 1

        # There should be some different elements, though by random chance
        # there could be some that stay the same
        self.assertGreater(different_elements, 0)

        # FREE SPACE should still be in the middle
        self.assertEqual(main.board[2][2], main.FREE_SPACE_TEXT)

        # Only FREE SPACE should be clicked
        self.assertEqual(len(main.clicked_tiles), 1)
        self.assertIn((2, 2), main.clicked_tiles)


if __name__ == "__main__":
    unittest.main()
