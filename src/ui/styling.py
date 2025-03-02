# UI styling functions
from nicegui import ui
from src.config.constants import (
    BOARD_TILE_FONT, BOARD_TILE_FONT_WEIGHT, 
    BOARD_TILE_FONT_STYLE
)

def get_line_style_for_lines(line_count: int, text_color: str) -> str:
    """Return a style string with adjusted line-height based on line count."""
    if line_count == 1:
        lh = "1.5em"  # More spacing for a single line
    elif line_count == 2:
        lh = "1.2em"  # Slightly reduced spacing for two lines
    elif line_count == 3:
        lh = "0.9em"  # Even tighter spacing for three lines
    else:
        lh = "0.7em"  # For four or more lines
        
    return f"font-family: '{BOARD_TILE_FONT}', sans-serif; font-weight: {BOARD_TILE_FONT_WEIGHT}; font-style: {BOARD_TILE_FONT_STYLE}; padding: 0; margin: 0; color: {text_color}; line-height: {lh};"

def get_google_font_css(font_name: str, weight: str, style: str, uniquifier: str) -> str:
    """Generate CSS for the specified Google font."""
    return f"""
<style>
.{uniquifier} {{
  font-family: "{font_name}", sans-serif;
  font-optical-sizing: auto;
  font-weight: {weight};
  font-style: {style};
}}
</style>
"""

def setup_head(background_color: str):
    """Set up common page head elements."""
    # Add Super Carnival font
    ui.add_css("""
        @font-face {
            font-family: 'Super Carnival';
            font-style: normal;
            font-weight: 400;
            src: url('/static/Super%20Carnival.woff') format('woff');
        }
    """)
    
    # Add Google Fonts
    ui.add_head_html(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family={BOARD_TILE_FONT.replace(" ", "+")}&display=swap" rel="stylesheet">
    """)
    
    # Add CSS class for board tile fonts
    ui.add_head_html(get_google_font_css(BOARD_TILE_FONT, BOARD_TILE_FONT_WEIGHT, BOARD_TILE_FONT_STYLE, "board_tile"))
    
    # Set background color
    ui.add_head_html(f'<style>body {{ background-color: {background_color}; }}</style>')