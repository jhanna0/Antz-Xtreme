from typing import List, Optional

from Pieces.source import Source
from Game.broadcast import broadcast
from Game.generate import Generator
from Managers.manager import Manager
from Game.definitions import source_rarity_weights, source_creation_rate, source_worth_map

class SourceManager(Manager[Source]):
    def __init__(self, generator: Generator):
        super().__init__()
        self.generator = generator
        self.potential_sources = (97, 123)

    # need a class to handle "find best location"
    def create_random_source(self):
        symbol = chr(self.generator.choose_from_range(self.potential_sources))
        location = self.generator.find_location_for_piece((2, 1))

        rarity = self.generator.choose_rarity(source_rarity_weights)
        creation_rate = self.generator.choose_from_list(source_creation_rate[rarity])
        worth = self.generator.choose_from_list(source_worth_map[rarity])
        self.register(Source(symbol, location, creation_rate, worth, rarity))
    
    def register(self, source: Source):
        super().register(source)
        broadcast.announce(f"{source.rarity.value} Resource {source.get_symbol()} has spawned!")

    def update(self):
        for source in self.get_pieces():
            source.grow()

    def get_best_source(self) -> Optional[Source]:
        return max(self.get_pieces(), key = lambda source: source.get_quantity(), default = None)
