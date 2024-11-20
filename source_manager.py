from board import Board
from source import Source
from typing import Dict

class SourceManager:
    def __init__(self, board: Board):
        self.sources: Dict[str, Source] = {}
        self.board = board

    def register(self, symbol: str, source: Source):
        self.sources[symbol] = source
        self.board.update_piece_position(self.sources)

    def update(self, game_time: float):
        for source in self.sources.values():
            source.try_to_create(game_time)
