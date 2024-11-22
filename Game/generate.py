from typing import Tuple, List, Dict
from random import randint, choice, choices

from Game.board import Board
from Game.definitions import Rarity

class Generator():
    def __init__(self, board: Board):
        self.board = board

    # we need to gracefully handle no position found
    def find_location_for_piece(self, piece_size: Tuple[int, int] = (1, 1), edge_preference: bool = False) -> Tuple[int, int]:
        rows, cols = self.board.get_size()
        width, height = piece_size

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

    def choose_from_list(self, items: List):
        return choice(items)

    def choose_from_range(self, range: Tuple[int, int]) -> int:
        return randint(range[0], range[1])

    def choose_rarity(self, weights: Dict) -> Rarity:
        return choices(
            population=list(weights.keys()),
            weights=list(weights.values()),
            k=1
        )[0]
