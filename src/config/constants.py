"""
Configuration constants for the Bingo application.
"""

# Header text and display settings
HEADER_TEXT = "COMMIT !BINGO"
HEADER_TEXT_COLOR = "#0CB2B3"
CLOSED_HEADER_TEXT = "Bingo Is Closed"
CLOSED_MESSAGE_TEXT = "GAME CLOSED"
CLOSED_MESSAGE_COLOR = "#FF7f33"

# Free space settings
FREE_SPACE_TEXT = "FREE MEAT"
FREE_SPACE_TEXT_COLOR = "#FF7f33"

# Tile appearance settings
TILE_CLICKED_BG_COLOR = "#100079"
TILE_CLICKED_TEXT_COLOR = "#1BEFF5"
TILE_UNCLICKED_BG_COLOR = "#1BEFF5"
TILE_UNCLICKED_TEXT_COLOR = "#100079"

# Page backgrounds
HOME_BG_COLOR = "#100079"
STREAM_BG_COLOR = "#00FF00"

# Font settings
HEADER_FONT_FAMILY = "'Super Carnival', sans-serif"
BOARD_TILE_FONT = "Inter"
BOARD_TILE_FONT_WEIGHT = "700"
BOARD_TILE_FONT_STYLE = "normal"

# UI Class Constants
BOARD_CONTAINER_CLASS = "flex justify-center items-center w-full"
HEADER_CONTAINER_CLASS = "w-full"
CARD_CLASSES = (
    "relative p-2 rounded-xl shadow-8 w-full h-full flex items-center justify-center"
)
COLUMN_CLASSES = "flex flex-col items-center justify-center gap-0 w-full"
GRID_CONTAINER_CLASS = "w-full aspect-square p-4"
GRID_CLASSES = "gap-2 h-full grid-rows-5"
ROW_CLASSES = "w-full"
LABEL_SMALL_CLASSES = "fit-text-small text-center select-none"
LABEL_CLASSES = "fit-text text-center select-none"
