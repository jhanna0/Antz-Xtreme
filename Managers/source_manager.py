from typing import List, Optional, Tuple

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
        location = self.generator.find_location_for_piece((1, 2)) # add source size to defintion

        rarity = self.generator.choose_rarity(source_rarity_weights)
        creation_rate = self.generator.choose_from_list(source_creation_rate[rarity])
        worth = self.generator.choose_from_list(source_worth_map[rarity])
        self.register(Source(symbol, location, creation_rate, worth, rarity))
    
    def register(self, source: Source):
        super().register(source)
        broadcast.announce(f"{source.rarity.value} Resource {source.get_symbol()} has spawned!")

    def update(self):
        remove_sources: List[Source] = []
        for source in self.get_pieces():
            if source.expired():
                remove_sources.append(source)
            source.grow()
        
        for source in remove_sources:
            self.remove_piece(source)

    def get_best_source(self, location: Tuple[int, int]) -> Optional[Source]:
        """
        Returns single source, first based off quantity + distance, then by just distance.
        """
        sources = self.get_pieces()
        
        # Attempt to find the closest non-depleted source
        non_depleted_sources = [source for source in sources if not source.is_depleted()]
        if non_depleted_sources:
            return min(non_depleted_sources, key=lambda source: source.get_distance_from(location))

        # Fallback to the closest source regardless of depletion
        return min(sources, key=lambda source: source.get_distance_from(location), default=None)
