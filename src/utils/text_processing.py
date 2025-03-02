# Text processing utilities
from typing import List

def split_phrase_into_lines(phrase: str, forced_lines: int = None) -> List[str]:
    """
    Split a phrase into multiple lines for better visual display.
    """
    words = phrase.split()
    n = len(words)
    
    if n <= 3:
        return words
    
    # Helper: total length of a list of words (including spaces between words)
    def segment_length(segment):
        return sum(len(word) for word in segment) + (len(segment) - 1 if segment else 0)
    
    candidates = []  # list of tuples: (number_of_lines, diff, candidate)
    
    # 2-line candidate
    best_diff_2 = float('inf')
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
        best_diff_3 = float('inf')
        best_seg_3 = None
        for i in range(1, n-1):
            for j in range(i+1, n):
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
        best_diff_4 = float('inf')
        best_seg_4 = None
        for i in range(1, n-2):
            for j in range(i+1, n-1):
                for k in range(j+1, n):
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
                        best_seg_4 = [" ".join(seg1), " ".join(seg2), " ".join(seg3), " ".join(seg4)]
        if best_seg_4 is not None:
            candidates.append((4, best_diff_4, best_seg_4))
    
    # If a forced number of lines is specified, try to return that candidate first
    if forced_lines is not None:
        forced_candidates = [cand for cand in candidates if cand[0] == forced_lines]
        if forced_candidates:
            _, _, best_candidate = min(forced_candidates, key=lambda x: x[1])
            return best_candidate
    
    # Otherwise, choose the candidate with the smallest diff
    if candidates:
        _, _, best_candidate = min(candidates, key=lambda x: x[1])
        return best_candidate
    else:
        # fallback (should never happen)
        return [" ".join(words)]