"""
Main entry point for the Bingo application.
"""

import logging
import os

from fastapi.staticfiles import StaticFiles
from nicegui import app, ui

from src.config.constants import FREE_SPACE_TEXT, HEADER_TEXT
from src.core.game_logic import (
    bingo_patterns,
    board,
    board_iteration,
    clicked_tiles,
    generate_board,
    is_game_closed,
    today_seed,
)
from src.ui.routes import init_routes
from src.utils.file_operations import read_phrases_file

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Initialize the application
def init_app():
    """Initialize the Bingo application."""

    # Initialize game state
    phrases = read_phrases_file()
    generate_board(board_iteration, phrases)

    # Initialize routes
    init_routes()

    # Mount the static directory
    app.add_static_files("/static", "static")
    # app.mount("/static", StaticFiles(directory="static"), name="static")

    return app


if __name__ in {"__main__", "__mp_main__"}:
    # Run the NiceGUI app
    init_app()
    ui.run(port=8080, title=f"{HEADER_TEXT}", dark=False)
