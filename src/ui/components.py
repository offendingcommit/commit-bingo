# Reusable UI components
from nicegui import ui
from typing import Dict, Callable, List, Tuple, Any

from src.config.constants import (
    HEADER_TEXT, HEADER_TEXT_COLOR, HEADER_FONT_FAMILY,
    BOARD_TILE_FONT, FREE_SPACE_TEXT, FREE_SPACE_TEXT_COLOR,
    TILE_CLICKED_BG_COLOR, TILE_CLICKED_TEXT_COLOR,
    TILE_UNCLICKED_BG_COLOR, TILE_UNCLICKED_TEXT_COLOR
)
from src.config.styles import (
    GRID_CONTAINER_CLASS, GRID_CLASSES,
    CARD_CLASSES, LABEL_CLASSES, LABEL_SMALL_CLASSES
)
from src.utils.text_processing import split_phrase_into_lines
from src.ui.styling import get_line_style_for_lines

def create_header():
    """Create the application header."""
    with ui.element("div").classes("w-full"):
        ui.label(f"{HEADER_TEXT}").classes("fit-header text-center").style(
            f"font-family: {HEADER_FONT_FAMILY}; color: {HEADER_TEXT_COLOR};"
        )

def create_board_controls(on_reset: Callable, on_new_board: Callable, seed_text: str):
    """Create board control buttons."""
    with ui.row().classes("w-full mt-4 items-center justify-center gap-4"):
        with ui.button("", icon="refresh", on_click=on_reset).classes("rounded-full w-12 h-12") as reset_btn:
            ui.tooltip("Reset Board")
        with ui.button("", icon="autorenew", on_click=on_new_board).classes("rounded-full w-12 h-12") as new_board_btn:
            ui.tooltip("New Board")
        seed_label = ui.label(f"Seed: {seed_text}").classes("text-sm text-center").style(
            f"font-family: '{BOARD_TILE_FONT}', sans-serif; color: {TILE_UNCLICKED_BG_COLOR};"
        )
    return seed_label