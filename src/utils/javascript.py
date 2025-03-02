# JavaScript integration utilities
import logging
from nicegui import ui

def run_fitty_js():
    """Run the fitty JavaScript library to resize text."""
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
        logging.debug(f"JavaScript execution failed (likely disconnected client): {e}")

def setup_javascript():
    """Add required JavaScript libraries to the page."""
    # Add fitty.js for text fitting
    ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/fitty@2.3.6/dist/fitty.min.js"></script>')
    
    # Add html2canvas for saving the board as image
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
    
        // Wait a short period to ensure that the board is fully rendered
        setTimeout(function() {
            html2canvas(boardElem, {
                useCORS: true,
                scale: 10,  // Increase scale for higher resolution
                logging: true,
                backgroundColor: null
            }).then(function(canvas) {
                var link = document.createElement('a');
                link.download = `bingo_board_${seed}.png`;
                link.href = canvas.toDataURL('image/png');
                link.click();
            });
        }, 500);
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
    
    # Add event listeners for responsive text resizing
    ui.add_head_html("""<script>
        // Run fitty when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(applyFitty, 100);
        });
        
        // Run fitty when window is resized
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(applyFitty, 100);
        });
        
        // Periodically check and reapply fitty for any dynamic changes
        setInterval(applyFitty, 1000);
    </script>""")