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
from src.core.state_manager import get_state_manager
from src.ui.routes import init_routes
from src.utils.file_operations import read_phrases_file

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Initialize the application
def init_app():
    """Initialize the Bingo application."""
    # Get the state manager (loads state from file if exists)
    state_manager = get_state_manager()
    
    # Check if we have existing state
    if state_manager.board:
        # Restore state from state manager
        logging.info("Game state loaded from server-side storage")
        # Update global variables from state manager
        import src.core.game_logic as game_logic
        game_logic.board = state_manager.board
        game_logic.clicked_tiles = state_manager.clicked_tiles
        game_logic.bingo_patterns = state_manager.bingo_patterns
        game_logic.board_iteration = state_manager.board_iteration
        game_logic.is_game_closed = state_manager.is_game_closed
        game_logic.today_seed = state_manager.today_seed
    else:
        # If no saved state exists, initialize fresh game state
        logging.info("No saved state found, initializing fresh game state")
        phrases = read_phrases_file()
        generated_board = generate_board(board_iteration, phrases)
        
        # Update state manager synchronously during initialization
        # We'll save to file after UI starts up
        import src.core.game_logic as game_logic
        
        # Use NiceGUI's app.on_startup to save initial state after event loop starts
        @app.on_startup
        async def save_initial_state():
            await state_manager.update_board(
                game_logic.board, 
                game_logic.board_iteration, 
                game_logic.today_seed
            )

    # Initialize routes
    init_routes()

    # Mount the static directory
    app.add_static_files("/static", "static")
    # app.mount("/static", StaticFiles(directory="static"), name="static")

    return app


if __name__ in {"__main__", "__mp_main__"}:
    # Run the NiceGUI app
    init_app()
    ui.run(port=8080, title=f"{HEADER_TEXT}", dark=False, storage_secret=os.getenv("STORAGE_SECRET","ThisIsMyCrappyStorageSecret"))
