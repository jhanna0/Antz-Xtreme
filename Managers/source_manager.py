from typing import List, Tuple, Optional
from random import randint, choice, choices, uniform

from Pieces.source import Source
from Game.broadcast import BroadCast
from Managers.manager import Manager
from Game.definitions import Rarity
from Game.definitions import source_rarity_worth_map, source_rarity_weights


class SourceManager(Manager[Source]):
    def __init__(self, potential_sources: List[str]):
        super().__init__()
        self.potential_sources = potential_sources

    # need a class to handle "find best location"
    def create_random_source(self, size: Tuple[int, int]):
        symbol = choice(self.potential_sources)
        location = (randint(0, size[0] - 1), randint(0, size[1] - 2)) # -2 for the text offset. handle w/ Piece.size

        # creation_rate should also be based on rarity
        rarity, creation_rate, worth = self._get_random_rarity(), uniform(1.0, 5.0), self._calculate_worth(rarity)
        self.register(Source(symbol, location, creation_rate, worth, rarity))
    
    def register(self, source: Source):
        super().register(source)
        BroadCast().announce(f"{source.rarity.value} Resource {source.get_symbol()} has spawned!")
    
    def get_best_source(self) -> Optional[Source]:
        return max(self.get_pieces(), key = lambda source: source.get_quantity(), default = None)
        
    def update(self, game_time: float):
        for source in self.get_pieces():
            source.try_to_create(game_time)

    def _get_random_rarity(self) -> Rarity:
        return choices(population=list(source_rarity_weights.keys()), weights=list(source_rarity_weights.values()), k=1)[0]

    # move this into rarity master class?
    def _calculate_worth(self, rarity: Rarity) -> int:
        min_worth, max_worth = source_rarity_worth_map[rarity]
        return randint(min_worth, max_worth)
