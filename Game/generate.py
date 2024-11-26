from typing import Tuple, List, Dict
from random import randint, choice, choices

from Game.board import Board
from Game.definitions import Rarity, source_rarity_weights, source_creation_rate, source_worth_map
from Managers.source_manager import SourceManager
from Pieces.source import Source
from Game.broadcast import broadcast


class Generator():
    def __init__(self, board: Board, sources: SourceManager):
        self.board = board
        self.sources = sources # probably don't need SourceManager dependency

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

    # need a method to handle "find best location"
    def create_random_source(self):
        symbol = chr(self.choose_from_range(self.sources.potential_sources))
        location = self.find_location_for_piece((1, 2)) # add source size to defintion

        rarity = self.choose_rarity(source_rarity_weights)
        creation_rate = self.choose_from_list(source_creation_rate[rarity])
        worth = self.choose_from_list(source_worth_map[rarity])
        source = Source(symbol, location, creation_rate, worth, rarity)
        self.sources.register(source)
