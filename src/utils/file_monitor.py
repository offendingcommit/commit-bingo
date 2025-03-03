"""
File monitoring utilities for the Bingo application.
"""

import logging
import os

from src.utils.file_operations import last_phrases_mtime, read_phrases_file


def check_phrases_file_change(update_callback):
    """
    Check if phrases.txt has changed. If so, re-read the file and call the update callback.

    Args:
        update_callback: Function to call with the new phrases when the file changes
    """
    global last_phrases_mtime
    try:
        mtime = os.path.getmtime("phrases.txt")
    except Exception as e:
        logging.error(f"Error checking phrases.txt: {e}")
        return

    if mtime != last_phrases_mtime:
        logging.info("phrases.txt changed, reloading board.")
        last_phrases_mtime = mtime

        # Re-read phrases.txt and invoke the callback
        phrases = read_phrases_file()
        update_callback(phrases)
