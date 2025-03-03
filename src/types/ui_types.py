"""
UI Type definitions for the Bingo application.
"""

from typing import Dict, List, Set, Tuple, Union

from nicegui import ui

# Basic types
Coordinate = Tuple[int, int]
BoardType = List[List[str]]
ClickedTiles = Set[Coordinate]
BingoPattern = str
BingoPatterns = Set[BingoPattern]

# UI Element types
TileLabelInfo = Dict[str, Union[ui.label, str]]
TileInfo = Dict[str, Union[ui.card, List[TileLabelInfo]]]
TileButtonsDict = Dict[Coordinate, TileInfo]
BoardViewTuple = Tuple[ui.element, TileButtonsDict]
BoardViews = Dict[str, BoardViewTuple]