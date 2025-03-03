"""
Controls UI module for the Bingo application.
"""

from nicegui import ui

from src.config.constants import BOARD_TILE_FONT, TILE_UNCLICKED_BG_COLOR
from src.core.game_logic import (
    close_game,
    controls_row,
    generate_new_board,
    reopen_game,
    reset_board,
    seed_label,
    today_seed,
)
from src.utils.file_operations import read_phrases_file


def create_controls_row():
    """
    Create the controls row with buttons for resetting the board, generating a new board, etc.
    Returns the created row element.
    """
    # These variables are defined in game_logic but need to be updated here

    phrases = read_phrases_file()

    with ui.row().classes("w-full mt-4 items-center justify-center gap-4") as row:
        with ui.button("", icon="refresh", on_click=lambda: reset_board()).classes(
            "rounded-full w-12 h-12"
        ) as reset_btn:
            ui.tooltip("Reset Board")
        with ui.button(
            "", icon="autorenew", on_click=lambda: generate_new_board(phrases)
        ).classes("rounded-full w-12 h-12") as new_board_btn:
            ui.tooltip("New Board")
        with ui.button("", icon="close", on_click=close_game).classes(
            "rounded-full w-12 h-12 bg-red-500"
        ) as close_btn:
            ui.tooltip("Close Game")
        ui_seed_label = (
            ui.label(f"Seed: {today_seed}")
            .classes("text-sm text-center")
            .style(
                f"font-family: '{BOARD_TILE_FONT}', sans-serif; color: {TILE_UNCLICKED_BG_COLOR};"
            )
        )

    # Store the controls row and seed label in the game_logic module
    from src.core.game_logic import controls_row, seed_label

    controls_row = row
    seed_label = ui_seed_label

    return row


def rebuild_controls_row(row):
    """
    Rebuild the controls row with all buttons after game is reopened.
    """
    phrases = read_phrases_file()

    row.clear()
    with row:
        with ui.button("", icon="refresh", on_click=lambda: reset_board()).classes(
            "rounded-full w-12 h-12"
        ) as reset_btn:
            ui.tooltip("Reset Board")
        with ui.button(
            "", icon="autorenew", on_click=lambda: generate_new_board(phrases)
        ).classes("rounded-full w-12 h-12") as new_board_btn:
            ui.tooltip("New Board")
        with ui.button("", icon="close", on_click=close_game).classes(
            "rounded-full w-12 h-12 bg-red-500"
        ) as close_btn:
            ui.tooltip("Close Game")
        ui_seed_label = (
            ui.label(f"Seed: {today_seed}")
            .classes("text-sm text-center")
            .style(
                f"font-family: '{BOARD_TILE_FONT}', sans-serif; color: {TILE_UNCLICKED_BG_COLOR};"
            )
        )

    # Update the seed label reference
    from src.core.game_logic import seed_label

    seed_label = ui_seed_label
