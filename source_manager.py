import random
from typing import Dict, List, Tuple
from source import Source
from board import Board

class SourceManager:
    def __init__(self, board: Board, potential_sources: List[str]):
        self.sources: Dict[str, Source] = {}
        self.board = board
        self.potential_sources = potential_sources
        self.board_size = self.board.get_board_size()

    # need to add logic to ensure this doesn't lay on a source already
    def register_random_source(self):
        """Randomly generate a new source with random properties."""
        symbol = random.choice(self.potential_sources)
        location = (
            random.randint(0, self.board_size[0] - 1),
            random.randint(0, self.board_size[1] - 1)
        )
        creation_rate = random.uniform(1.0, 5.0)  # Random creation rate between 1 and 5 seconds
        worth = random.randint(1, 10)  # Random worth between 1 and 10

        new_source = Source(symbol, location, creation_rate, worth)
        self.sources[symbol] = new_source
        self.board.update_piece_position(self.sources)

    def update(self, game_time: float):
        for source in self.sources.values():
            source.try_to_create(game_time)
