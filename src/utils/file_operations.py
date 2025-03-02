"""
File operation utilities for the Bingo application.
"""

import logging
import os

# Global variable to track phrases.txt modification time.
last_phrases_mtime = os.path.getmtime("phrases.txt")

def has_too_many_repeats(phrase, threshold=0.5):
    """
    Returns True if too many of the words in the phrase repeat.
    For example, if the ratio of unique words to total words is less than the threshold.
    Logs a debug message if the phrase is discarded.
    """
    words = phrase.split()
    if not words:
        return False
    unique_count = len(set(words))
    ratio = unique_count / len(words)
    if ratio < threshold:
        logging.debug(f"Discarding phrase '{phrase}' due to repeats: {unique_count}/{len(words)} = {ratio:.2f} < {threshold}")
        return True
    return False

def read_phrases_file():
    """
    Read phrases from phrases.txt, removing duplicates and filtering phrases with too many repeats.
    Returns a list of unique, valid phrases.
    """
    with open("phrases.txt", "r") as f:
        raw_phrases = [line.strip().upper() for line in f if line.strip()]

    # Remove duplicates while preserving order.
    unique_phrases = []
    seen = set()
    for p in raw_phrases:
        if p not in seen:
            seen.add(p)
            unique_phrases.append(p)

    # Filter out phrases with too many repeated words.
    return [p for p in unique_phrases if not has_too_many_repeats(p)]