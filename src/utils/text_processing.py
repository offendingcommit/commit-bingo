"""
Text processing utilities for the Bingo application.
"""

from src.config.constants import (
    BOARD_TILE_FONT,
    BOARD_TILE_FONT_STYLE,
    BOARD_TILE_FONT_WEIGHT,
)


def split_phrase_into_lines(phrase: str, forced_lines: int = None) -> list:
    """
    Splits the phrase into balanced lines.
    For phrases of up to 3 words, return one word per line.
    For longer phrases, try splitting the phrase into 2, 3, or 4 lines so that the total
    number of characters (including spaces) in each line is as similar as possible.
    The function will never return more than 4 lines.
    If 'forced_lines' is provided (2, 3, or 4), then the candidate with that many lines is chosen
    if available; otherwise, the best candidate overall is returned.
    """
    words = phrase.split()
    n = len(words)
    if n <= 3:
        return words

    # Helper: total length of a list of words (including spaces between words).
    def segment_length(segment):
        return sum(len(word) for word in segment) + (len(segment) - 1 if segment else 0)

    candidates = []  # list of tuples: (number_of_lines, diff, candidate)

    # 2-line candidate
    best_diff_2 = float("inf")
    best_seg_2 = None
    for i in range(1, n):
        seg1 = words[:i]
        seg2 = words[i:]
        len1 = segment_length(seg1)
        len2 = segment_length(seg2)
        diff = abs(len1 - len2)
        if diff < best_diff_2:
            best_diff_2 = diff
            best_seg_2 = [" ".join(seg1), " ".join(seg2)]
    if best_seg_2 is not None:
        candidates.append((2, best_diff_2, best_seg_2))

    # 3-line candidate (if at least 4 words)
    if n >= 4:
        best_diff_3 = float("inf")
        best_seg_3 = None
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                seg1 = words[:i]
                seg2 = words[i:j]
                seg3 = words[j:]
                len1 = segment_length(seg1)
                len2 = segment_length(seg2)
                len3 = segment_length(seg3)
                current_diff = max(len1, len2, len3) - min(len1, len2, len3)
                if current_diff < best_diff_3:
                    best_diff_3 = current_diff
                    best_seg_3 = [" ".join(seg1), " ".join(seg2), " ".join(seg3)]
        if best_seg_3 is not None:
            candidates.append((3, best_diff_3, best_seg_3))

    # 4-line candidate (if at least 5 words)
    if n >= 5:
        best_diff_4 = float("inf")
        best_seg_4 = None
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    seg1 = words[:i]
                    seg2 = words[i:j]
                    seg3 = words[j:k]
                    seg4 = words[k:]
                    len1 = segment_length(seg1)
                    len2 = segment_length(seg2)
                    len3 = segment_length(seg3)
                    len4 = segment_length(seg4)
                    diff = max(len1, len2, len3, len4) - min(len1, len2, len3, len4)
                    if diff < best_diff_4:
                        best_diff_4 = diff
                        best_seg_4 = [
                            " ".join(seg1),
                            " ".join(seg2),
                            " ".join(seg3),
                            " ".join(seg4),
                        ]
        if best_seg_4 is not None:
            candidates.append((4, best_diff_4, best_seg_4))

    # If a forced number of lines is specified, try to return that candidate first.
    if forced_lines is not None:
        forced_candidates = [cand for cand in candidates if cand[0] == forced_lines]
        if forced_candidates:
            _, _, best_candidate = min(forced_candidates, key=lambda x: x[1])
            return best_candidate

    # Otherwise, choose the candidate with the smallest diff.
    if candidates:
        _, _, best_candidate = min(candidates, key=lambda x: x[1])
        return best_candidate
    else:
        # fallback (should never happen)
        return [" ".join(words)]


def get_line_style_for_lines(line_count: int, default_text_color: str) -> str:
    """
    Return a complete style string with an adjusted line-height based on the number of lines
    that resulted from splitting the phrase.
    Fewer lines (i.e. unsplit phrases) get a higher line-height, while more lines get a lower one.
    """
    if line_count == 1:
        lh = "1.5em"  # More spacing for a single line.
    elif line_count == 2:
        lh = "1.2em"  # Slightly reduced spacing for two lines.
    elif line_count == 3:
        lh = "0.9em"  # Even tighter spacing for three lines.
    else:
        lh = "0.7em"  # For four or more lines.
    return f"font-family: '{BOARD_TILE_FONT}', sans-serif; font-weight: {BOARD_TILE_FONT_WEIGHT}; font-style: {BOARD_TILE_FONT_STYLE}; padding: 0; margin: 0; color: {default_text_color}; line-height: {lh};"


def get_google_font_css(
    font_name: str, weight: str, style: str, uniquifier: str
) -> str:
    """
    Returns a CSS style block defining a class for the specified Google font.
    'uniquifier' is used as the CSS class name.
    """
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
