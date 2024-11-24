from typing import Set

from Pieces.ability import Ability
from Managers.manager import Manager
from Game.board import Board
from Game.tick import ticks
from Game.broadcast import broadcast

class AbilityManager(Manager[Ability]):
    def __init__(self, board: Board):
        super().__init__()
        self.board = board
        self.cool_down = 2 # probably could go into Character class
        self.last_ability = 0 # probably could go into Character class
    
    def try_to_register(self, ability: Ability) -> None:
        current_tick = ticks.get_current_tick()
        if current_tick - self.last_ability >= self.cool_down:
            self.register(ability)
            self.last_ability = current_tick

    def update(self) -> None:
        self.apply_effects()
        self.clear_invalid_abilities()
        for ability in self.get_pieces():
            ability.prepare_next_turn() # i think this step is extraneous
    
    def apply_effects(self) -> None:
        # we could even have ability responsible for which managers to check (prevents projectile from removing source)
        for ability in self.get_pieces():
            ability.take_action()

    def clear_invalid_abilities(self):
        self.pieces = [piece for piece in self.get_pieces() if piece.validate_next_turn()]
