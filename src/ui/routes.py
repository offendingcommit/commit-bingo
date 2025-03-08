"""
Routes module for the Bingo application.
"""

import logging
import json

from nicegui import app, ui

from src.config.constants import HOME_BG_COLOR, STREAM_BG_COLOR
from src.ui.board_builder import create_board_view
from src.ui.sync import sync_board_state


@ui.page("/")
def home_page():
    """
    Main page with the interactive bingo board and controls.
    """
    create_board_view(HOME_BG_COLOR, True)
    try:
        # Create a timer that deactivates when the client disconnects
        timer = ui.timer(0.1, sync_board_state)
        app.on_disconnect(timer.cancel)
    except Exception as e:
        logging.warning(f"Error creating timer: {e}")


@ui.page("/stream")
def stream_page():
    """
    Stream view of the bingo board (without controls, for display purposes).
    """
    create_board_view(STREAM_BG_COLOR, False)
    try:
        # Create a timer that deactivates when the client disconnects
        timer = ui.timer(0.1, sync_board_state)
        app.on_disconnect(timer.cancel)
    except Exception as e:
        logging.warning(f"Error creating timer: {e}")


@app.get("/health")
def health():
    return json.dumps({"health": "ok"}, indent=4, sort_keys=True)


def init_routes():
    """
    Initialize routes and return any necessary objects.
    This is mainly a placeholder to ensure routes are imported
    and decorated properly.
    """
    return None
