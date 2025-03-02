# Board UI construction
from nicegui import ui
import logging
from typing import Dict, Callable, List, Tuple, Any

from src.config.constants import (
    FREE_SPACE_TEXT, FREE_SPACE_TEXT_COLOR,
    TILE_CLICKED_BG_COLOR, TILE_CLICKED_TEXT_COLOR,
    TILE_UNCLICKED_BG_COLOR, TILE_UNCLICKED_TEXT_COLOR
)
from src.config.styles import (
    GRID_CONTAINER_CLASS, GRID_CLASSES, CARD_CLASSES,
    LABEL_CLASSES, LABEL_SMALL_CLASSES
)
from src.utils.text_processing import split_phrase_into_lines
from src.ui.styling import get_line_style_for_lines
from src.utils.javascript import run_fitty_js

def build_board(parent, board: List[List[str]], clicked_tiles: set, tile_buttons_dict: dict, on_tile_click: Callable):
    """Build the Bingo board UI."""
    with parent:
        with ui.element("div").classes(GRID_CONTAINER_CLASS):
            with ui.grid(columns=5).classes(GRID_CLASSES):
                for row_idx, row in enumerate(board):
                    for col_idx, phrase in enumerate(row):
                        card = ui.card().classes(CARD_CLASSES).style("cursor: pointer;")
                        labels_list = []  # initialize list for storing label metadata
                        
                        with card:
                            with ui.column().classes("flex flex-col items-center justify-center gap-0 w-full"):
                                default_text_color = FREE_SPACE_TEXT_COLOR if phrase.upper() == FREE_SPACE_TEXT else TILE_UNCLICKED_TEXT_COLOR
                                lines = split_phrase_into_lines(phrase)
                                line_count = len(lines)
                                
                                for line in lines:
                                    with ui.row().classes("w-full items-center justify-center"):
                                        base_class = LABEL_SMALL_CLASSES if len(line) <= 3 else LABEL_CLASSES
                                        lbl = ui.label(line).classes(base_class).style(
                                            get_line_style_for_lines(line_count, default_text_color)
                                        )
                                        labels_list.append({
                                            "ref": lbl,
                                            "base_classes": base_class,
                                            "base_style": get_line_style_for_lines(line_count, default_text_color)
                                        })
                                        
                        tile_buttons_dict[(row_idx, col_idx)] = {"card": card, "labels": labels_list}
                        
                        if phrase.upper() == FREE_SPACE_TEXT:
                            clicked_tiles.add((row_idx, col_idx))
                            card.style(f"color: {FREE_SPACE_TEXT_COLOR}; border: none; outline: 3px solid {TILE_CLICKED_TEXT_COLOR};")
                        else:
                            card.on("click", lambda e, r=row_idx, c=col_idx: on_tile_click(r, c))
                            
    return tile_buttons_dict

def update_tile_styles(board: List[List[str]], clicked_tiles: set, tile_buttons_dict: dict):
    """Update styles for each tile based on clicked state."""
    for (r, c), tile in tile_buttons_dict.items():
        phrase = board[r][c]
        
        if (r, c) in clicked_tiles:
            new_card_style = f"background-color: {TILE_CLICKED_BG_COLOR}; color: {TILE_CLICKED_TEXT_COLOR}; border: none; outline: 3px solid {TILE_CLICKED_TEXT_COLOR};"
            new_label_color = TILE_CLICKED_TEXT_COLOR
        else:
            new_card_style = f"background-color: {TILE_UNCLICKED_BG_COLOR}; color: {TILE_UNCLICKED_TEXT_COLOR}; border: none;"
            new_label_color = TILE_UNCLICKED_TEXT_COLOR
        
        # Update the card style
        tile["card"].style(new_card_style)
        tile["card"].update()
        
        # Recalculate the styles for labels
        lines = split_phrase_into_lines(phrase)
        line_count = len(lines)
        new_label_style = get_line_style_for_lines(line_count, new_label_color)
        
        # Update all label elements for this tile
        for label_info in tile["labels"]:
            lbl = label_info["ref"]
            lbl.classes(label_info["base_classes"])
            lbl.style(new_label_style)
            lbl.update()
    
    # Run fitty JavaScript to resize text
    run_fitty_js()