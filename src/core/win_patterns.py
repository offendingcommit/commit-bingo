# Win condition detection
from typing import List, Set, Tuple
from nicegui import ui

# Global state
bingo_patterns = set()

def check_winner(clicked_tiles: Set[Tuple[int, int]]) -> List[str]:
    """Check for winning patterns and return newly found ones."""
    global bingo_patterns
    new_patterns = []
    
    # Check rows and columns
    for i in range(5):
        if all((i, j) in clicked_tiles for j in range(5)):
            if f"row{i}" not in bingo_patterns:
                new_patterns.append(f"row{i}")
        if all((j, i) in clicked_tiles for j in range(5)):
            if f"col{i}" not in bingo_patterns:
                new_patterns.append(f"col{i}")
    
    # Check main diagonal
    if all((i, i) in clicked_tiles for i in range(5)):
        if "diag_main" not in bingo_patterns:
            new_patterns.append("diag_main")
    
    # Check anti-diagonal
    if all((i, 4-i) in clicked_tiles for i in range(5)):
        if "diag_anti" not in bingo_patterns:
            new_patterns.append("diag_anti")
    
    # Special patterns
    
    # Blackout: every cell is clicked
    if all((r, c) in clicked_tiles for r in range(5) for c in range(5)):
        if "blackout" not in bingo_patterns:
            new_patterns.append("blackout")
    
    # 4 Corners
    if all(pos in clicked_tiles for pos in [(0,0), (0,4), (4,0), (4,4)]):
        if "four_corners" not in bingo_patterns:
            new_patterns.append("four_corners")
    
    # Plus shape
    plus_cells = {(2, c) for c in range(5)} | {(r, 2) for r in range(5)}
    if all(cell in clicked_tiles for cell in plus_cells):
        if "plus" not in bingo_patterns:
            new_patterns.append("plus")
    
    # X shape
    if all((i, i) in clicked_tiles for i in range(5)) and all((i, 4-i) in clicked_tiles for i in range(5)):
        if "x_shape" not in bingo_patterns:
            new_patterns.append("x_shape")
    
    # Perimeter
    perimeter_cells = {(0, c) for c in range(5)} | {(4, c) for c in range(5)} | {(r, 0) for r in range(5)} | {(r, 4) for r in range(5)}
    if all(cell in clicked_tiles for cell in perimeter_cells):
        if "perimeter" not in bingo_patterns:
            new_patterns.append("perimeter")
    
    return new_patterns

def process_win_notifications(new_patterns: List[str]) -> None:
    """Process new win patterns and show appropriate notifications."""
    global bingo_patterns
    
    if not new_patterns:
        return
        
    # Separate new win patterns into standard and special ones
    special_set = {"blackout", "four_corners", "plus", "x_shape", "perimeter"}
    standard_new = [p for p in new_patterns if p not in special_set]
    special_new = [p for p in new_patterns if p in special_set]
    
    # Process standard win conditions
    if standard_new:
        for pattern in standard_new:
            bingo_patterns.add(pattern)
        standard_total = sum(1 for p in bingo_patterns if p not in special_set)
        
        if standard_total == 1:
            message = "BINGO!"
        elif standard_total == 2:
            message = "DOUBLE BINGO!"
        elif standard_total == 3:
            message = "TRIPLE BINGO!"
        elif standard_total == 4:
            message = "QUADRUPLE BINGO!"
        elif standard_total == 5:
            message = "QUINTUPLE BINGO!"
        else:
            message = f"{standard_total}-WAY BINGO!"
            
        ui.notify(message, color="green", duration=5)
    
    # Process special win conditions
    for sp in special_new:
        bingo_patterns.add(sp)
        sp_message = sp.replace("_", " ").title() + " Bingo!"
        ui.notify(sp_message, color="blue", duration=5)