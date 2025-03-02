# Main entry point for the application
import logging
from nicegui import ui, app
from fastapi.staticfiles import StaticFiles

# Import our modules
from src.config.constants import HEADER_TEXT
from src.ui.pages import setup_pages, home_page, stream_page
from src.core.phrases import initialize_phrases
from src.core.board import generate_board, board_iteration

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Initialize core components
    initialize_phrases()
    
    # Generate initial board
    generate_board(board_iteration)
    
    # Set up routes and pages
    setup_pages()
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Run the app
    ui.run(port=8080, title=f"{HEADER_TEXT}", dark=False)

if __name__ in {"__main__", "__mp_main__"}:
    main()