from nicegui import ui
import random
import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# List of 24 phrases (excluding the center "FREE MEAT")
phrases = [
    "CAN'T HAVE NICE THINGS", "TECHNO BABBLE", "HELL YEAH!", "WE GET A RAID", "NOICE",
    "POSITION ONE", "HOWS MY AUDIO", "SOMEONE REDEEMS HYDRATE", "THREATEN GOOD TIME", "MENTIONS MODS",
    "SAYS TEXAS", "SPINS BONUS WHEEL", "JOIN DISCORD", "HOLY SMOKES",
    "SAYS CATS OR DOGS", "DOOT DOOTS", "MAKES AIR QUOTES", "TALKS ABOUT ELLEE", "ZOOM",
    "SIGHT LINES", "TALKS ABOUT PALIA", "SAYS DISCORD", "DANCE PARTY", "THATS NUTS!"
]

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

# Function to create the Bingo board UI
def create_bingo_board():
    logging.info("Creating Bingo board")
    ui.label("Commit Bingo!").classes("text-3xl font-bold mt-4 text-yellow-400")
    ui.label(f"Seed: {today_seed}").classes("text-md text-gray-300")

    with ui.element("div").classes("flex justify-center items-center w-full"):
        with ui.grid(columns=5).classes("gap-2 mt-4"):
            for row_idx, row in enumerate(board):
                for col_idx, phrase in enumerate(row):
                    # Create a clickable card for this cell with reduced padding and centered content.
                    card = ui.card().classes("p-2 bg-yellow-500 hover:bg-yellow-400 rounded-lg w-full flex items-center justify-center").style("cursor: pointer; aspect-ratio: 1;")
                    with card:
                        with ui.column().classes("flex flex-col items-center justify-center gap-0 w-full"):
                            # Split the phrase into words and make each word a separate label.
                            for word in phrase.split():
                                tile = ui.label(word).classes("text-lg text-center")
                                tile.style("font-family: 'Super Carnival', sans-serif; padding: 0; margin: 0;")
                    # Save the card reference.
                    tile_buttons[(row_idx, col_idx)] = card
                    # When the card is clicked, toggle its state.
                    card.on("click", lambda e, r=row_idx, c=col_idx: toggle_tile(r, c))

# Toggle tile click state (for example usage)
def toggle_tile(row, col):
    key = (row, col)
    if key in clicked_tiles:
        logging.debug(f"Tile at {key} unclicked")
        clicked_tiles.remove(key)
        tile_buttons[key].style("background: #facc15; border: none;")
    else:
        logging.debug(f"Tile at {key} clicked")
        clicked_tiles.add(key)
        tile_buttons[key].style("color: #22c55e; border: 15px solid #15803d;")

    check_winner()

# Check for Bingo win condition
def check_winner():
    for i in range(5):
        if all((i, j) in clicked_tiles for j in range(5)) or all((j, i) in clicked_tiles for j in range(5)):
            ui.notify("BINGO!", color="green", duration=5)
            return
    if all((i, i) in clicked_tiles for i in range(5)) or all((i, 4 - i) in clicked_tiles for i in range(5)):
        ui.notify("BINGO!", color="green", duration=5)

# Set up NiceGUI page and head elements
ui.page("/")
ui.add_head_html('<link href="https://fonts.cdnfonts.com/css/super-carnival" rel="stylesheet">')
create_bingo_board()
ui.run(port=8080, title="Commit Bingo", dark=True)
