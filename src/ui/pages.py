# Page definitions
from nicegui import ui
import logging
from typing import Dict, Tuple, List, Set, Any

from src.config.constants import (
    HOME_BG_COLOR, STREAM_BG_COLOR
)
from src.core.board import (
    board, clicked_tiles, board_views, 
    generate_board, reset_board, generate_new_board,
    toggle_tile, today_seed
)
from src.core.win_patterns import check_winner, process_win_notifications
from src.core.phrases import check_phrases_file_change
from src.ui.styling import setup_head
from src.ui.components import create_header, create_board_controls
from src.ui.board_view import build_board, update_tile_styles
from src.utils.javascript import setup_javascript, run_fitty_js

# Global variable for the seed label
seed_label = None

def toggle_tile_handler(row: int, col: int):
    """Handle tile click events."""
    toggle_tile(row, col)
    
    # Check for win conditions
    new_patterns = check_winner(clicked_tiles)
    process_win_notifications(new_patterns)
    
    # Update all board views
    sync_board_state()

def sync_board_state():
    """Synchronize the board state across all views."""
    try:
        # Update tile styles in every board view
        for view_key, (container, tile_buttons_local) in board_views.items():
            update_tile_styles(board, clicked_tiles, tile_buttons_local)
            container.update()
        
        # Run fitty to resize text
        run_fitty_js()
    except Exception as e:
        logging.debug(f"Error in sync_board_state: {e}")

def create_board_view(background_color: str, is_global: bool):
    """Create a board view (home or stream)."""
    # Setup page head elements
    setup_head(background_color)
    setup_javascript()
    
    # Create header
    create_header()
    
    # Create board container
    if is_global:
        container = ui.element("div").classes("home-board-container flex justify-center items-center w-full")
        try:
            ui.run_javascript("document.querySelector('.home-board-container').id = 'board-container'")
        except Exception as e:
            logging.debug(f"Setting board container ID failed: {e}")
    else:
        container = ui.element("div").classes("stream-board-container flex justify-center items-center w-full")
        try:
            ui.run_javascript("document.querySelector('.stream-board-container').id = 'board-container-stream'")
        except Exception as e:
            logging.debug(f"Setting stream container ID failed: {e}")
    
    if is_global:
        # For home view, use global state
        global seed_label
        tile_buttons_dict = {}
        build_board(container, board, clicked_tiles, tile_buttons_dict, toggle_tile_handler)
        board_views["home"] = (container, tile_buttons_dict)
        
        # Add phrase file watcher
        try:
            check_timer = ui.timer(1, check_phrases_file_change)
        except Exception as e:
            logging.warning(f"Error setting up timer: {e}")
        
        # Add board controls
        seed_label = create_board_controls(reset_board, generate_new_board, today_seed)
    else:
        # For stream view, create local state
        local_tile_buttons = {}
        build_board(container, board, clicked_tiles, local_tile_buttons, toggle_tile_handler)
        board_views["stream"] = (container, local_tile_buttons)

@ui.page("/")
def home_page():
    """Home page with interactive board."""
    logging.info("Creating home page with board...")
    # Ensure we have a board before trying to render it
    from src.core.board import board
    if not board or len(board) == 0:
        logging.warning("Board is empty in home_page! Regenerating...")
        from src.core.board import generate_board, board_iteration
        generate_board(board_iteration)
    
    # Create the board view
    create_board_view(HOME_BG_COLOR, True)
    
    try:
        # Create a timer that deactivates when the client disconnects
        timer = ui.timer(0.1, sync_board_state)
        logging.info("Home page sync timer created successfully")
    except Exception as e:
        logging.warning(f"Error creating home page timer: {e}")
    
    # Make sure JS is executed for text fitting
    try:
        from src.utils.javascript import run_fitty_js
        ui.timer(0.5, run_fitty_js)
    except Exception as e:
        logging.warning(f"Error setting up fitty timer: {e}")
    
    return "Home page loaded"  # Return something to confirm the function ran

@ui.page("/stream")
def stream_page():
    """Stream overlay page."""
    logging.info("Creating stream page with board...")
    # Ensure we have a board before trying to render it
    from src.core.board import board
    if not board or len(board) == 0:
        logging.warning("Board is empty in stream_page! Regenerating...")
        from src.core.board import generate_board, board_iteration
        generate_board(board_iteration)
    
    # Create the board view
    create_board_view(STREAM_BG_COLOR, False)
    
    try:
        # Create a timer that deactivates when the client disconnects
        timer = ui.timer(0.1, sync_board_state)
        logging.info("Stream page sync timer created successfully")
    except Exception as e:
        logging.warning(f"Error creating stream page timer: {e}")
    
    # Make sure JS is executed for text fitting
    try:
        from src.utils.javascript import run_fitty_js
        ui.timer(0.5, run_fitty_js)
    except Exception as e:
        logging.warning(f"Error setting up fitty timer: {e}")
    
    return "Stream page loaded"  # Return something to confirm the function ran

def setup_pages():
    """Initialize all pages."""
    # Explicitly register the routes
    # This ensures they're properly set up even if NiceGUI has trouble with decorators
    # We use direct calls instead of just referencing to make sure they're active
    logging.info("Setting up page routes...")
    
    # These will register routes due to the @ui.page decorators
    if not getattr(home_page, "_is_registered", False):
        logging.info("Registering home page route...")
        home_page()
        home_page._is_registered = True
    
    if not getattr(stream_page, "_is_registered", False):
        logging.info("Registering stream page route...")
        stream_page()
        stream_page._is_registered = True
    
    logging.info("Page routes registered successfully")