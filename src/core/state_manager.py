"""
Server-side state management for the Bingo application.

This module provides a centralized state manager that persists game state
to the server's file system instead of relying on client-side storage.
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple

from src.config.constants import FREE_SPACE_TEXT

if TYPE_CHECKING:
    from src.types.ui_types import BingoPatterns, BoardType, ClickedTiles, Coordinate
else:
    # Define types locally to avoid circular imports in tests
    BoardType = List[List[str]]
    ClickedTiles = Set[Tuple[int, int]]
    BingoPatterns = Set[str]
    Coordinate = Tuple[int, int]


@dataclass
class GameState:
    """Represents the complete game state."""
    board: BoardType = field(default_factory=list)
    clicked_tiles: ClickedTiles = field(default_factory=set)
    bingo_patterns: BingoPatterns = field(default_factory=set)
    is_game_closed: bool = False
    board_iteration: int = 1
    today_seed: Optional[str] = None
    header_text: str = "BINGO!"
    timestamp: float = field(default_factory=time.time)


class GameStateManager:
    """
    Manages game state with server-side persistence.
    
    This replaces the client-side app.storage.general approach with
    a proper server-side file storage solution.
    """
    
    def __init__(self, state_file: Path = Path("game_state.json")):
        """Initialize the state manager."""
        self.state_file = state_file
        self._state = GameState()
        self._lock = asyncio.Lock()
        self._save_lock = asyncio.Lock()
        self._save_task = None
        self._pending_save = False
        
        # Load existing state on initialization
        self._load_state_sync()
    
    def _load_state_sync(self) -> bool:
        """Synchronously load state from file (for initialization)."""
        if not self.state_file.exists():
            logging.info("No existing state file found, starting fresh")
            return False
        
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
            
            # Validate and restore state
            self._state = GameState(
                board=data.get('board', []),
                clicked_tiles=set(tuple(pos) for pos in data.get('clicked_tiles', [])),
                bingo_patterns=set(data.get('bingo_patterns', [])),
                is_game_closed=data.get('is_game_closed', False),
                board_iteration=data.get('board_iteration', 1),
                today_seed=data.get('today_seed'),
                header_text=data.get('header_text', 'BINGO!'),
                timestamp=data.get('timestamp', time.time())
            )
            
            logging.info(f"State loaded from {self.state_file}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to load state: {e}")
            return False
    
    async def load_state(self) -> bool:
        """Asynchronously load state from file."""
        async with self._lock:
            return self._load_state_sync()
    
    async def save_state(self, immediate: bool = False) -> bool:
        """
        Save state to file with debouncing.
        
        Args:
            immediate: If True, save immediately without debouncing
        """
        if immediate:
            return await self._persist()
        
        # Mark that we need to save
        self._pending_save = True
        
        # Cancel existing save task if any
        if self._save_task and not self._save_task.done():
            self._save_task.cancel()
        
        # Schedule a new save
        self._save_task = asyncio.create_task(self._debounced_save())
        return True
    
    async def _debounced_save(self):
        """Save state after a short delay to batch updates."""
        try:
            # Wait a bit for more changes
            await asyncio.sleep(0.5)
            
            if self._pending_save:
                await self._persist()
                self._pending_save = False
                
        except asyncio.CancelledError:
            # Task was cancelled, that's fine
            pass
    
    async def _persist(self) -> bool:
        """Persist state to file atomically."""
        async with self._save_lock:
            try:
                # Prepare state data
                state_dict = {
                    'board': self._state.board,
                    'clicked_tiles': list(self._state.clicked_tiles),
                    'bingo_patterns': list(self._state.bingo_patterns),
                    'is_game_closed': self._state.is_game_closed,
                    'board_iteration': self._state.board_iteration,
                    'today_seed': self._state.today_seed,
                    'header_text': self._state.header_text,
                    'timestamp': time.time()
                }
                
                # Atomic write using temp file
                temp_file = self.state_file.with_suffix('.tmp')
                with open(temp_file, 'w') as f:
                    json.dump(state_dict, f, indent=2)
                
                # Atomic rename
                temp_file.rename(self.state_file)
                
                logging.debug(f"State saved to {self.state_file}")
                return True
                
            except Exception as e:
                logging.error(f"Failed to save state: {e}")
                return False
    
    async def toggle_tile(self, row: int, col: int) -> bool:
        """Toggle a tile's clicked state."""
        async with self._lock:
            pos = (row, col)
            
            if pos in self._state.clicked_tiles:
                self._state.clicked_tiles.remove(pos)
                clicked = False
            else:
                self._state.clicked_tiles.add(pos)
                clicked = True
            
            # Save state asynchronously
            await self.save_state()
            
            return clicked
    
    async def reset_board(self) -> None:
        """Reset all clicked tiles."""
        async with self._lock:
            self._state.clicked_tiles.clear()
            self._state.bingo_patterns.clear()
            
            # Add free space back if board exists
            if len(self._state.board) > 2:
                free_pos = (2, 2)
                if self._state.board[2][2] == FREE_SPACE_TEXT:
                    self._state.clicked_tiles.add(free_pos)
            
            await self.save_state()
    
    async def close_game(self) -> None:
        """Close the game."""
        async with self._lock:
            self._state.is_game_closed = True
            await self.save_state()
    
    async def reopen_game(self) -> None:
        """Reopen the game."""
        async with self._lock:
            self._state.is_game_closed = False
            await self.save_state()
    
    async def update_board(self, board: BoardType, iteration: int, 
                          seed: Optional[str] = None) -> None:
        """Update the board configuration."""
        async with self._lock:
            self._state.board = board
            self._state.board_iteration = iteration
            self._state.today_seed = seed
            
            # Reset clicked tiles for new board
            self._state.clicked_tiles.clear()
            self._state.bingo_patterns.clear()
            
            # Add free space
            if len(board) > 2 and len(board[2]) > 2:
                if board[2][2] == FREE_SPACE_TEXT:
                    self._state.clicked_tiles.add((2, 2))
            
            await self.save_state()
    
    async def update_header_text(self, text: str) -> None:
        """Update the header text."""
        async with self._lock:
            self._state.header_text = text
            await self.save_state()
    
    async def add_bingo_pattern(self, pattern: str) -> None:
        """Add a winning bingo pattern."""
        async with self._lock:
            self._state.bingo_patterns.add(pattern)
            await self.save_state()
    
    # Property accessors (read-only)
    @property
    def board(self) -> BoardType:
        """Get current board."""
        return self._state.board.copy()
    
    @property
    def clicked_tiles(self) -> ClickedTiles:
        """Get clicked tiles."""
        return self._state.clicked_tiles.copy()
    
    @property
    def is_game_closed(self) -> bool:
        """Check if game is closed."""
        return self._state.is_game_closed
    
    @property
    def board_iteration(self) -> int:
        """Get board iteration."""
        return self._state.board_iteration
    
    @property
    def today_seed(self) -> Optional[str]:
        """Get today's seed."""
        return self._state.today_seed
    
    @property
    def header_text(self) -> str:
        """Get header text."""
        return self._state.header_text
    
    @property
    def bingo_patterns(self) -> BingoPatterns:
        """Get bingo patterns."""
        return self._state.bingo_patterns.copy()
    
    def get_full_state(self) -> Dict[str, Any]:
        """Get the complete game state as a dictionary."""
        return {
            'board': self._state.board,
            'clicked_tiles': list(self._state.clicked_tiles),
            'bingo_patterns': list(self._state.bingo_patterns),
            'is_game_closed': self._state.is_game_closed,
            'board_iteration': self._state.board_iteration,
            'today_seed': self._state.today_seed,
            'header_text': self._state.header_text,
            'timestamp': self._state.timestamp
        }


# Global state manager instance
_state_manager: Optional[GameStateManager] = None


def get_state_manager() -> GameStateManager:
    """Get or create the global state manager instance."""
    global _state_manager
    if _state_manager is None:
        _state_manager = GameStateManager()
    return _state_manager