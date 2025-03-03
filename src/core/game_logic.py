"""
Core game logic for the Bingo application.
"""

import datetime
import logging
import random

from nicegui import ui

from src.config.constants import (
    CLOSED_HEADER_TEXT,
    FREE_SPACE_TEXT,
    FREE_SPACE_TEXT_COLOR,
    HEADER_TEXT,
    TILE_CLICKED_BG_COLOR,
    TILE_CLICKED_TEXT_COLOR,
    TILE_UNCLICKED_BG_COLOR,
    TILE_UNCLICKED_TEXT_COLOR,
)
from src.utils.text_processing import get_line_style_for_lines, split_phrase_into_lines

# Global variables for game state
board = []  # 2D array of phrases
clicked_tiles = set()  # Set of (row, col) tuples that are clicked
bingo_patterns = set()  # Set of winning patterns found
board_iteration = 1
is_game_closed = False
today_seed = None

# Global variables for UI references (initialized in the UI module)
header_label = None
controls_row = None
seed_label = None
board_views = {}  # Dictionary mapping view name to (container, tile_buttons) tuple


def generate_board(seed_val: int, phrases):
    """
    Generate a new board using the provided seed value.
    Also resets the clicked_tiles (ensuring the FREE SPACE is clicked) and sets the global today_seed.
    """
    global board, today_seed, clicked_tiles

    todays_seed = datetime.date.today().strftime("%Y%m%d")
    random.seed(seed_val)

    shuffled_phrases = random.sample(phrases, 24)
    shuffled_phrases.insert(12, FREE_SPACE_TEXT)

    board = [shuffled_phrases[i : i + 5] for i in range(0, 25, 5)]

    clicked_tiles.clear()
    for r, row in enumerate(board):
        for c, phrase in enumerate(row):
            if phrase.upper() == FREE_SPACE_TEXT:
                clicked_tiles.add((r, c))

    today_seed = f"{todays_seed}.{seed_val}"

    return board


def toggle_tile(row, col):
    """
    Toggle the state of a tile (clicked/unclicked).
    Updates the UI and checks for winner.
    """
    global clicked_tiles

    # Don't allow toggling the free space
    if (row, col) == (2, 2):
        return

    key = (row, col)
    if key in clicked_tiles:
        clicked_tiles.remove(key)
    else:
        clicked_tiles.add(key)

    check_winner()

    for view_key, (container, tile_buttons_local) in board_views.items():
        for (r, c), tile in tile_buttons_local.items():
            phrase = board[r][c]
            if (r, c) in clicked_tiles:
                new_card_style = f"background-color: {TILE_CLICKED_BG_COLOR}; color: {TILE_CLICKED_TEXT_COLOR}; border: none; outline: 3px solid {TILE_CLICKED_TEXT_COLOR};"
                new_label_color = TILE_CLICKED_TEXT_COLOR
            else:
                new_card_style = f"background-color: {TILE_UNCLICKED_BG_COLOR}; color: {TILE_UNCLICKED_TEXT_COLOR}; border: none;"
                new_label_color = TILE_UNCLICKED_TEXT_COLOR

            tile["card"].style(new_card_style)
            lines = split_phrase_into_lines(phrase)
            line_count = len(lines)
            new_label_style = get_line_style_for_lines(line_count, new_label_color)

            for label_info in tile["labels"]:
                lbl = label_info["ref"]
                lbl.classes(label_info["base_classes"])
                lbl.style(new_label_style)
                lbl.update()

            tile["card"].update()

        container.update()

    try:
        js_code = """
            setTimeout(function() {
                if (typeof fitty !== 'undefined') {
                    fitty('.fit-text', { multiLine: true, minSize: 10, maxSize: 1000 });
                    fitty('.fit-text-small', { multiLine: true, minSize: 10, maxSize: 72 });
                }
            }, 50);
        """
        ui.run_javascript(js_code)
    except Exception as e:
        logging.debug(f"JavaScript execution failed: {e}")


def check_winner():
    """
    Check for Bingo win condition and update the UI accordingly.
    """
    global bingo_patterns
    new_patterns = []

    # Check rows and columns.
    for i in range(5):
        if all((i, j) in clicked_tiles for j in range(5)):
            if f"row{i}" not in bingo_patterns:
                new_patterns.append(f"row{i}")
        if all((j, i) in clicked_tiles for j in range(5)):
            if f"col{i}" not in bingo_patterns:
                new_patterns.append(f"col{i}")

    # Check main diagonal.
    if all((i, i) in clicked_tiles for i in range(5)):
        if "diag_main" not in bingo_patterns:
            new_patterns.append("diag_main")

    # Check anti-diagonal.
    if all((i, 4 - i) in clicked_tiles for i in range(5)):
        if "diag_anti" not in bingo_patterns:
            new_patterns.append("diag_anti")

    # Additional winning variations:

    # Blackout: every cell is clicked.
    if all((r, c) in clicked_tiles for r in range(5) for c in range(5)):
        if "blackout" not in bingo_patterns:
            new_patterns.append("blackout")

    # 4 Corners: top-left, top-right, bottom-left, bottom-right.
    if all(pos in clicked_tiles for pos in [(0, 0), (0, 4), (4, 0), (4, 4)]):
        if "four_corners" not in bingo_patterns:
            new_patterns.append("four_corners")

    # Plus shape: complete center row and center column.
    plus_cells = {(2, c) for c in range(5)} | {(r, 2) for r in range(5)}
    if all(cell in clicked_tiles for cell in plus_cells):
        if "plus" not in bingo_patterns:
            new_patterns.append("plus")

    # X shape: both diagonals complete.
    if all((i, i) in clicked_tiles for i in range(5)) and all(
        (i, 4 - i) in clicked_tiles for i in range(5)
    ):
        if "x_shape" not in bingo_patterns:
            new_patterns.append("x_shape")

    # Outside edges (perimeter): all border cells clicked.
    perimeter_cells = (
        {(0, c) for c in range(5)}
        | {(4, c) for c in range(5)}
        | {(r, 0) for r in range(5)}
        | {(r, 4) for r in range(5)}
    )
    if all(cell in clicked_tiles for cell in perimeter_cells):
        if "perimeter" not in bingo_patterns:
            new_patterns.append("perimeter")

    if new_patterns:
        # Separate new win patterns into standard and special ones.
        special_set = {"blackout", "four_corners", "plus", "x_shape", "perimeter"}
        standard_new = [p for p in new_patterns if p not in special_set]
        special_new = [p for p in new_patterns if p in special_set]

        # Process standard win conditions (rows, columns, diagonals).
        if standard_new:
            for pattern in standard_new:
                bingo_patterns.add(pattern)
            standard_total = sum(1 for p in bingo_patterns if p not in special_set)
            if standard_total == 1:
                message = "BINGO!"
            elif standard_total == 2:
                message = "DOUBLE BINGO!"
            elif standard_total == 3:
                message = "TRIPLE BINGO!"
            elif standard_total == 4:
                message = "QUADRUPLE BINGO!"
            elif standard_total == 5:
                message = "QUINTUPLE BINGO!"
            else:
                message = f"{standard_total}-WAY BINGO!"
            ui.notify(message, color="green", duration=5)

        # Process special win conditions individually.
        for sp in special_new:
            bingo_patterns.add(sp)
            # Format the name to title-case and append "Bingo!"
            sp_message = sp.replace("_", " ").title() + " Bingo!"
            ui.notify(sp_message, color="blue", duration=5)


def reset_board():
    """
    Reset the board by clearing all clicked states, clearing winning patterns,
    and re-adding the FREE SPACE.
    """
    global bingo_patterns
    bingo_patterns.clear()  # Clear previously recorded wins.
    clicked_tiles.clear()
    for r, row in enumerate(board):
        for c, phrase in enumerate(row):
            if phrase.upper() == FREE_SPACE_TEXT:
                clicked_tiles.add((r, c))


def generate_new_board(phrases):
    """
    Generate a new board with an incremented iteration seed and update all board views.
    """
    global board_iteration
    board_iteration += 1
    generate_board(board_iteration, phrases)

    # Update all board views (both home and stream)
    from src.ui.board_builder import build_board

    for view_key, (container, tile_buttons_local) in board_views.items():
        container.clear()
        tile_buttons_local.clear()
        build_board(container, tile_buttons_local, toggle_tile, board, clicked_tiles)
        container.update()

    # Update the seed label if available
    if "seed_label" in globals() and seed_label:
        seed_label.set_text(f"Seed: {today_seed}")
        seed_label.update()

    reset_board()


def close_game():
    """
    Close the game - hide the board and update the header text.
    This function is called when the close button is clicked.
    """
    global is_game_closed, header_label
    is_game_closed = True

    # Update header text on the current view
    if header_label:
        header_label.set_text(CLOSED_HEADER_TEXT)
        header_label.update()

    # Hide all board views (both home and stream)
    for view_key, (container, tile_buttons_local) in board_views.items():
        container.style("display: none;")
        container.update()

    # Modify the controls row to only show the New Board button
    if controls_row:
        controls_row.clear()
        with controls_row:
            with ui.button("", icon="autorenew", on_click=reopen_game).classes(
                "rounded-full w-12 h-12"
            ) as new_game_btn:
                ui.tooltip("Start New Game")

    # Update stream page as well - this will trigger sync_board_state on connected clients
    # Note: ui.broadcast() was used in older versions of NiceGUI, but may not be available
    try:
        ui.broadcast()  # Broadcast changes to all connected clients
    except AttributeError:
        # In newer versions of NiceGUI, broadcast might not be available
        # We rely on the timer-based sync instead
        logging.info("ui.broadcast not available, relying on timer-based sync")
        
        # If broadcast isn't available, manually trigger sync on current view
        # This ensures immediate update even if broadcast fails
        from src.ui.sync import sync_board_state
        sync_board_state()

    # Notify that game has been closed
    ui.notify("Game has been closed", color="red", duration=3)


def reopen_game():
    """
    Reopen the game after it has been closed.
    This regenerates a new board and resets the UI.
    """
    global is_game_closed, header_label, board_iteration

    # Reset game state
    is_game_closed = False

    # Update header text back to original for the current view
    if header_label:
        header_label.set_text(HEADER_TEXT)
        header_label.update()

    # Generate a new board
    from src.utils.file_operations import read_phrases_file

    phrases = read_phrases_file()

    board_iteration += 1
    generate_board(board_iteration, phrases)

    # Rebuild the controls row with all buttons
    from src.ui.controls import rebuild_controls_row

    if controls_row:
        rebuild_controls_row(controls_row)

    # Recreate and show all board views
    from src.ui.board_builder import build_board

    for view_key, (container, tile_buttons_local) in board_views.items():
        container.style("display: block;")
        container.clear()
        tile_buttons_local.clear()
        build_board(container, tile_buttons_local, toggle_tile, board, clicked_tiles)
        container.update()

    # Reset clicked tiles except for FREE SPACE
    reset_board()

    # Notify that a new game has started
    ui.notify("New game started", color="green", duration=3)

    # Update stream page and all other connected clients
    # This will trigger sync_board_state on all clients including the stream view
    try:
        ui.broadcast()  # Broadcast changes to all connected clients
    except AttributeError:
        # In newer versions of NiceGUI, broadcast might not be available
        # Run sync manually to ensure immediate update
        logging.info("ui.broadcast not available, relying on timer-based sync")
        
        # If broadcast isn't available, manually trigger sync on current view
        # This ensures immediate update even if broadcast fails
        from src.ui.sync import sync_board_state
        sync_board_state()
