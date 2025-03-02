# Phrase loading and processing
import os
import logging
from typing import List

# Global variables
phrases = []
last_phrases_mtime = 0

def has_too_many_repeats(phrase: str, threshold=0.5) -> bool:
    """Returns True if too many words in the phrase repeat."""
    words = phrase.split()
    if not words:
        return False
    unique_count = len(set(words))
    ratio = unique_count / len(words)
    if ratio < threshold:
        logging.debug(f"Discarding phrase '{phrase}' due to repeats: {unique_count}/{len(words)} = {ratio:.2f} < {threshold}")
        return True
    return False

def load_phrases() -> List[str]:
    """Load and process phrases from phrases.txt."""
    global phrases, last_phrases_mtime
    
    try:
        last_phrases_mtime = os.path.getmtime("phrases.txt")
        
        with open("phrases.txt", "r") as f:
            raw_phrases = [line.strip().upper() for line in f if line.strip()]
            
        # Remove duplicates while preserving order
        unique_phrases = []
        seen = set()
        for p in raw_phrases:
            if p not in seen:
                seen.add(p)
                unique_phrases.append(p)
                
        # Filter out phrases with too many repeated words
        phrases = [p for p in unique_phrases if not has_too_many_repeats(p)]
        return phrases
        
    except Exception as e:
        logging.error(f"Error loading phrases: {e}")
        return []

def initialize_phrases() -> None:
    """Initialize phrases during app startup."""
    load_phrases()

def get_phrases() -> List[str]:
    """Get the current phrases list."""
    return phrases

def check_phrases_file_change() -> bool:
    """Check if phrases.txt has changed and reload if needed."""
    global last_phrases_mtime
    
    try:
        mtime = os.path.getmtime("phrases.txt")
        if mtime != last_phrases_mtime:
            logging.info("phrases.txt changed, reloading phrases.")
            load_phrases()
            return True
    except Exception as e:
        logging.error(f"Error checking phrases.txt: {e}")
    
    return False