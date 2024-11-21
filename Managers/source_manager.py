import random
from typing import Dict, List
from Pieces.source import Source, Rarity
from Game.board import Board
from Game.broadcast import BroadCast
from Managers.manager import Manager

class SourceManager(Manager):
    def __init__(self, board: Board, potential_sources: List[str]):
        super().__init__()
        self.board = board
        self.potential_sources = potential_sources

    def _get_random_rarity(self) -> Rarity:
        """Determine the rarity of the source using weighted probabilities."""
        rarity_weights = {
            Rarity.COMMON: 70,     
            Rarity.UNCOMMON: 20,  
            Rarity.RARE: 9,       
            Rarity.LEGENDARY: 1   # 1% chance
        }
        return random.choices(
            population=list(rarity_weights.keys()),
            weights=list(rarity_weights.values()),
            k=1
        )[0]

    # yup move this into rarity master class
    def _calculate_worth(self, rarity: Rarity) -> int:
        """Calculate the worth of a source based on its rarity."""
        rarity_worth_map = {
            Rarity.COMMON: (1, 5),      
            Rarity.UNCOMMON: (6, 10),   
            Rarity.RARE: (11, 20),     
            Rarity.LEGENDARY: (21, 50)
        }
        min_worth, max_worth = rarity_worth_map[rarity]
        return random.randint(min_worth, max_worth)

    def create_random_source(self):
        """Register a new source with random properties and rarity."""
        self.board_size = self.board.get_board_size()

        # Generate random source properties
        # -2 for the text offset
        symbol = random.choice(self.potential_sources)
        location = (
            random.randint(0, self.board_size[0] - 1),
            random.randint(0, self.board_size[1] - 2)
        )

        # creation_rate should also be based on rarity
        creation_rate = random.uniform(1.0, 5.0)
        rarity = self._get_random_rarity()
        worth = self._calculate_worth(rarity)

        # Create and register the source
        new_source = Source(symbol, location, creation_rate, worth, rarity)
        self.register(new_source)
    
    def register(self, source: Source):
        super().register(source)
        BroadCast().announce(f"{source.rarity.value} Resource {source.get_symbol()} has spawned!")
        
    def update(self, game_time: float):
        """Update all sources and attempt to create items."""
        for source in self.get_piece_array():
            source.try_to_create(game_time)
