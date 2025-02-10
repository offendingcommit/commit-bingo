from nicegui import ui
import random
import datetime
import logging
import asyncio

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Read phrases from a text file and convert them to uppercase.
with open("phrases.txt", "r") as f:
    phrases = [line.strip().upper() for line in f if line.strip()]

# Use today's date as the seed for deterministic shuffling
today_seed = datetime.date.today().strftime("%Y%m%d")
random.seed(int(today_seed))  # Everyone gets the same shuffle per day

# Shuffle and create the 5x5 board:
shuffled_phrases = random.sample(phrases, 24)  # Random but fixed order per day
shuffled_phrases.insert(12, "FREE MEAT")         # Center slot
board = [shuffled_phrases[i:i+5] for i in range(0, 25, 5)]

# Track clicked tiles and store chip references
clicked_tiles = set()
tile_buttons = {}  # {(row, col): chip}
tile_icons = {}  # {(row, col): icon reference}
admin_checkboxes = {}  # {(row, col): admin checkbox element}

def split_phrase_into_lines(phrase: str) -> list:
    """
    Splits the phrase into balanced lines.
    If the phrase has two or fewer words, return it as a single line.
    Otherwise, split into two lines at the midpoint.
    """
    words = phrase.split()
    if len(words) == 1:
        return [words[0]]
    elif len(words) == 2:
        return [words[0], words[1]]
    else:
        mid = round(len(words) / 2)
        return [" ".join(words[:mid]), " ".join(words[mid:])]

# Function to create the Bingo board UI
def create_bingo_board():
    # The header and seed label are handled outside this function.
    logging.info("Creating Bingo board")

    with ui.element("div").classes("flex justify-center items-center w-full"):
         with ui.element("div").classes("w-full max-w-3xl aspect-square"):
              with ui.grid(columns=5).classes("gap-2 h-full grid-rows-5"):
                for row_idx, row in enumerate(board):
                    for col_idx, phrase in enumerate(row):
                        # Create a clickable card for this cell with reduced padding and centered content. Added 'relative' class for icon overlay.
                        card = ui.card().classes("relative p-2 bg-yellow-500 hover:bg-yellow-400 rounded-lg w-full h-full flex items-center justify-center").style("cursor: pointer;")
                        with card:
                            with ui.column().classes("flex flex-col items-center justify-center gap-0 w-full"):
                                # Set text color: free meat gets #FF7f33, others black
                                default_text_color = "#FF7f33" if phrase.upper() == "FREE MEAT" else "black"
                                for line in split_phrase_into_lines(phrase):
                                    ui.label(line).classes("fit-text text-center select-none").style(f"font-family: 'Super Carnival', sans-serif; padding: 0; margin: 0; color: {default_text_color};")
                        # After the column, add a hidden check icon overlay
                        icon = ui.icon("check").classes("absolute inset-0 m-auto text-3xl text-white").style("display: none;")
                        tile_buttons[(row_idx, col_idx)] = card
                        tile_icons[(row_idx, col_idx)] = icon
                        if phrase.upper() == "FREE MEAT":
                            clicked_tiles.add((row_idx, col_idx))
                            card.style("color: #FF7f33; background: #facc15; border: none;")
                            icon.style("display: block;")
                        else:
                            card.on("click", lambda e, r=row_idx, c=col_idx: toggle_tile(r, c))

# Toggle tile click state (for example usage)
def toggle_tile(row, col):
    # Do not allow toggling for the FREE MEAT cell (center cell)
    if (row, col) == (2, 2):
        return
    key = (row, col)
    if key in clicked_tiles:
        logging.debug(f"Tile at {key} unclicked")
        clicked_tiles.remove(key)
    else:
        logging.debug(f"Tile at {key} clicked")
        clicked_tiles.add(key)
    check_winner()
    sync_board_state()

# Check for Bingo win condition
def check_winner():
    for i in range(5):
        if all((i, j) in clicked_tiles for j in range(5)) or all((j, i) in clicked_tiles for j in range(5)):
            ui.notify("BINGO!", color="green", duration=5)
            return
    if all((i, i) in clicked_tiles for i in range(5)) or all((i, 4 - i) in clicked_tiles for i in range(5)):
        ui.notify("BINGO!", color="green", duration=5)

def sync_board_state():
    # Sync the styles of each tile according to the global clicked_tiles
    for r in range(5):
        for c in range(5):
            key = (r, c)
            # Skip updating the FREE MEAT cell
            if board[r][c].upper() == "FREE MEAT":
                continue
            if key in clicked_tiles:
                tile_buttons[key].style("background: #22c55e; color: white; border: none;")
                tile_icons[key].style("display: block;")
            else:
                tile_buttons[key].style("background: #facc15; border: none; color: black;")
                tile_icons[key].style("display: none;")
            tile_buttons[key].update()
            tile_icons[key].update()
    # --- New: update admin panel checkboxes when board state syncs ---
    sync_admin_checkboxes()
    update_admin_visibility()

def sync_admin_checkboxes():
    """
    Sync the values in both copies of each admin checkbox with the global clicked_tiles.
    """
    for key, chks in admin_checkboxes.items():
        new_value = key in clicked_tiles
        if chks["left"].value != new_value:
            chks["left"].value = new_value
            chks["left"].update()
        if chks["right"].value != new_value:
            chks["right"].value = new_value
            chks["right"].update()

def update_admin_visibility():
    """
    Bind the visibility of the admin checkboxes:
       - left copy is visible only when unchecked (value False)
       - right copy is visible only when checked (value True)
    """
    for key, chks in admin_checkboxes.items():
        val = chks["left"].value  # both copies hold the same value
        chks["left"].visible = not val  # show left box only when unchecked
        chks["right"].visible = val     # show right box only when checked
        chks["left"].update()
        chks["right"].update()

def admin_checkbox_change(e, key):
    # When a checkbox in the admin page is toggled, update the global clicked_tiles
    if e.value:
        clicked_tiles.add(key)
    else:
        clicked_tiles.discard(key)
    sync_board_state()

# Set up NiceGUI page and head elements
ui.page("/")
ui.add_head_html('<link href="https://fonts.cdnfonts.com/css/super-carnival" rel="stylesheet">')
ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/fitty@2.3.6/dist/fitty.min.js"></script>')
ui.add_head_html('<style>body { background-color: #100079; }</style>')

with ui.element("div").classes("w-full max-w-3xl mx-auto"):
    ui.label("COMMIT BINGO!").classes("fit-header text-center").style("font-family: 'Super Carnival', sans-serif; color: #0CB2B3;")

create_bingo_board()

# Add a timer that calls sync_board_state every 1 second to push state updates to all clients
ui.timer(1, sync_board_state)

with ui.element("div").classes("w-full mt-4"):
    ui.label(f"Seed: {today_seed}").classes("text-md text-gray-300 text-center")

ui.add_head_html("""<script>
  document.addEventListener('DOMContentLoaded', () => {
    fitty('.fit-text', { multiLine: true, maxSize: 100 });
    fitty('.fit-header', { multiLine: true, maxSize: 200 });
  });
  window.addEventListener('resize', () => {
    fitty('.fit-text', { multiLine: true, maxSize: 100 });
    fitty('.fit-header', { multiLine: true, maxSize: 200 });
  });
</script>""")

@ui.page("/admin")
def admin_page():
    with ui.column().classes("w-full max-w-xl mx-auto p-4") as container:
        ui.label("Admin Panel (Seed Phrases)").classes("text-h4 text-center")
        panel = ui.column()  # container for the checkboxes row

        def build_admin_panel():
            panel.clear()  # clear previous panel content
            with panel:        # add new content as children of panel
                with ui.row():
                    with ui.column().classes("w-1/2"):
                        ui.label("Uncalled").classes("text-h5 text-center")
                        # Create left (uncalled) checkboxes inside this column.
                        for r in range(5):
                            for c in range(5):
                                key = (r, c)
                                phrase = board[r][c]
                                def on_admin_checkbox_change(e, key=key):
                                    if e.value:
                                        clicked_tiles.add(key)
                                    else:
                                        clicked_tiles.discard(key)
                                    sync_board_state()
                                    update_admin_visibility()
                                    build_admin_panel()  # re-render admin panel after change
                                left_chk = ui.checkbox(phrase, value=(key in clicked_tiles), on_change=on_admin_checkbox_change)
                                admin_checkboxes.setdefault(key, {})["left"] = left_chk
                    with ui.column().classes("w-1/2"):
                        ui.label("Called").classes("text-h5 text-center")
                        # Create right (called) checkboxes inside this column.
                        for r in range(5):
                            for c in range(5):
                                key = (r, c)
                                phrase = board[r][c]
                                def on_admin_checkbox_change(e, key=key):
                                    if e.value:
                                        clicked_tiles.add(key)
                                    else:
                                        clicked_tiles.discard(key)
                                    sync_board_state()
                                    update_admin_visibility()
                                    build_admin_panel()  # re-render admin panel after change
                                right_chk = ui.checkbox(phrase, value=(key in clicked_tiles), on_change=on_admin_checkbox_change)
                                admin_checkboxes.setdefault(key, {})["right"] = right_chk

        build_admin_panel()
        ui.timer(1, update_admin_visibility)

ui.run(port=8080, title="Commit Bingo", dark=False)
