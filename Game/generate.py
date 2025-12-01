from typing import Tuple, List, Dict, Any, Callable, TYPE_CHECKING
from random import randint, choice, choices

from Game.board import Board
from Game.definitions import Rarity

if TYPE_CHECKING:
    from Managers.entity_manager import EntityManager

class Generator():
    def __init__(self, board: Board, manager: 'EntityManager'):
        self.board = board
        self.manager = manager
    
    def choose_from_range(self, range_tuple: Tuple[int, int]) -> int:
        """Choose a random integer from a range (start, end)."""
        return randint(range_tuple[0], range_tuple[1])
    
    def choose_from_list(self, values: Tuple[int, int]) -> int:
        """Choose a random value from the tuple range."""
        return randint(values[0], values[1])
    
    def choose_rarity(self, weights: Dict[Rarity, int]) -> Rarity:
        """Choose a rarity based on weighted probabilities."""
        rarities = list(weights.keys())
        probabilities = list(weights.values())
        return choices(rarities, weights=probabilities, k=1)[0]
        
    # we need to gracefully handle no position found !!! -> board just won't place it
    def find_location_for_piece(self, piece_size: Tuple[int, int] = (1, 1), edge_preference: bool = False) -> Tuple[int, int]:
        rows, cols = self.board.get_size()
        width, height = piece_size

        # I don't like how this is the only non-deterministic method in the app
        if edge_preference:
            # Try to place near edges first
            for _ in range(50):  # Limit edge attempts
                x, y = self._get_edge_location(rows, cols, width, height)
                if self.board.can_place(piece_size, (x, y)):
                    return (x, y)

        # Fall back to random placement
        for _ in range(100):
            x = randint(0, rows - height)
            y = randint(0, cols - width)
            if self.board.can_place(piece_size, (x, y)):
                return (x, y)

        return (-1, -1)

    def _get_edge_location(self, rows, cols, width, height) -> Tuple[int, int]:
        """Randomly choose an edge: 'top', 'bottom', 'left', or 'right'"""
        edge = choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            x = 0
            y = randint(0, cols - width)
        elif edge == 'bottom':
            x = rows - height
            y = randint(0, cols - width)
        elif edge == 'left':
            x = randint(0, rows - height)
            y = 0
        elif edge == 'right':
            x = randint(0, rows - height)
            y = cols - width
        return (x, y)
