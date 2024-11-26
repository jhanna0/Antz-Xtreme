from typing import List, Optional, Tuple

from Pieces.source import Source
from Game.broadcast import broadcast
from Managers.manager import Manager

class SourceManager(Manager[Source]):
    def __init__(self):
        super().__init__()
        self.potential_sources = (97, 123)
    
    def register(self, source: Source) -> None:
        super().register(source)
        # broadcast.announce(f"{source.rarity.value} Resource {source.get_symbol()} has spawned!")

    def turn_sequence(self) -> None:
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
