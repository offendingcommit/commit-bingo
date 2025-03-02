"""
Head setup module for the Bingo application.
"""

import logging
from nicegui import ui

from src.config.constants import (
    BOARD_TILE_FONT,
    BOARD_TILE_FONT_STYLE,
    BOARD_TILE_FONT_WEIGHT,
    HEADER_FONT_FAMILY,
    HEADER_TEXT,
    HEADER_TEXT_COLOR
)
from src.utils.text_processing import get_google_font_css


def setup_head(background_color: str):
    """
    Set up common head elements: fonts, fitty JS, and background color.
    """
    # Set the header label in the game_logic module
    from src.core.game_logic import header_label
    
    ui.add_css("""
        
            @font-face {
                font-family: 'Super Carnival';
                font-style: normal;
                font-weight: 400;
                /* Load the local .woff file from the static folder (URL-encoded for Safari) */
                src: url('/static/Super%20Carnival.woff') format('woff');
            }
        
    """)
    
    ui.add_head_html(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family={BOARD_TILE_FONT.replace(" ", "+")}&display=swap" rel="stylesheet">
    """)
    
    # Add CSS class for board tile fonts
    ui.add_head_html(get_google_font_css(BOARD_TILE_FONT, BOARD_TILE_FONT_WEIGHT, BOARD_TILE_FONT_STYLE, "board_tile"))
    
    # Add fitty.js for text resizing
    ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/fitty@2.3.6/dist/fitty.min.js"></script>')
    
    # Add html2canvas library and capture function.
    ui.add_head_html("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
    function captureBoardAndDownload(seed) {
        var boardElem = document.getElementById('board-container');
        if (!boardElem) {
            alert("Board container not found!");
            return;
        }
        // Run fitty to ensure text is resized and centered
        if (typeof fitty !== 'undefined') {
            fitty('.fit-text', { multiLine: true, minSize: 10, maxSize: 1000 });
            fitty('.fit-text-small', { multiLine: true, minSize: 10, maxSize: 72 });
        }
    
        // Wait a short period to ensure that the board is fully rendered and styles have settled.
        setTimeout(function() {
            html2canvas(boardElem, {
                useCORS: true,
                scale: 10,  // Increase scale for higher resolution
                logging: true,
                backgroundColor: null
            }).then(function(canvas) {
                var link = document.createElement('a');
                link.download = `bingo_board_${seed}.png`;  // Include seed in filename
                link.href = canvas.toDataURL('image/png');
                link.click();
            });
        }, 500);  // Adjust delay if necessary
    }
    
    // Function to safely apply fitty
    function applyFitty() {
        if (typeof fitty !== 'undefined') {
            fitty('.fit-text', { multiLine: true, minSize: 10, maxSize: 1000 });
            fitty('.fit-text-small', { multiLine: true, minSize: 10, maxSize: 72 });
            fitty('.fit-header', { multiLine: true, minSize: 10, maxSize: 2000 });
        }
    }
    </script>
    """)
    
    # Set background color
    ui.add_head_html(f'<style>body {{ background-color: {background_color}; }}</style>')
    
    # Add event listeners for fitty
    ui.add_head_html("""<script>
        // Run fitty when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(applyFitty, 100);  // Slight delay to ensure all elements are rendered
        });
        
        // Run fitty when window is resized
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(applyFitty, 100);  // Debounce resize events
        });
        
        // Periodically check and reapply fitty for any dynamic changes
        setInterval(applyFitty, 1000);
    </script>""")
    
    # Create header with full width
    with ui.element("div").classes("w-full"):
        ui_header_label = ui.label(f"{HEADER_TEXT}").classes("fit-header text-center").style(f"font-family: {HEADER_FONT_FAMILY}; color: {HEADER_TEXT_COLOR};")
        
    # Make the header label available in game_logic module
    from src.core.game_logic import header_label
    header_label = ui_header_label