# Board generation and management
import random
import datetime
from typing import List, Dict, Set, Tuple

from src.config.constants import FREE_SPACE_TEXT, FREE_SPACE_POSITION
# Avoid import at module level to prevent circular imports
# We'll import get_phrases inside the function

# Global state
board = []
clicked_tiles = set()
board_iteration = 1
today_seed = ""
board_views = {}

def generate_board(seed_val: int) -> List[List[str]]:
    """Generate a new board using the provided seed value."""
    global board, today_seed, clicked_tiles
    
    # Import here to avoid circular imports
    from src.core.phrases import get_phrases
    import logging
    
    todays_seed = datetime.date.today().strftime("%Y%m%d")
    random.seed(seed_val)
    
    # Get phrases and check if we have enough
    phrases = get_phrases()
    if not phrases or len(phrases) < 24:
        logging.error(f"Not enough phrases available! Found {len(phrases)} phrases, need at least 24.")
        # Add fallback phrases if necessary
        if not phrases:
            logging.warning("Using fallback phrases")
            phrases = [f"Phrase {i}" for i in range(1, 30)]
    
    # Sample phrases and add FREE_SPACE
    shuffled_phrases = random.sample(phrases, 24)
    shuffled_phrases.insert(12, FREE_SPACE_TEXT)
    
    # Create board as 5x5 grid
    board = [shuffled_phrases[i:i+5] for i in range(0, 25, 5)]
    
    # Clear and re-add FREE_SPACE to clicked tiles
    clicked_tiles.clear()
    for r, row in enumerate(board):
        for c, phrase in enumerate(row):
            if phrase.upper() == FREE_SPACE_TEXT:
                clicked_tiles.add((r, c))
                logging.debug(f"Added FREE_SPACE at position ({r}, {c})")
                
    today_seed = f"{todays_seed}.{seed_val}"
    logging.info(f"Board generated with seed {today_seed}, {len(board)} rows x {len(board[0])} columns")
    return board

def reset_board() -> None:
    """Clear all clicked tiles except FREE SPACE."""
    global clicked_tiles
    clicked_tiles.clear()
    for r, row in enumerate(board):
        for c, phrase in enumerate(row):
            if phrase.upper() == FREE_SPACE_TEXT:
                clicked_tiles.add((r, c))

def generate_new_board() -> None:
    """Generate a completely new board with a new seed."""
    global board_iteration
    board_iteration += 1
    return generate_board(board_iteration)

def toggle_tile(row: int, col: int) -> None:
    """Toggle the clicked state of a tile."""
    if (row, col) == FREE_SPACE_POSITION:
        return
        
    key = (row, col)
    if key in clicked_tiles:
        clicked_tiles.remove(key)
    else:
        clicked_tiles.add(key)