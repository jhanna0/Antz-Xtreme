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
        self.cool_down = 2 # how can we handle cooldowns by ability by character?
        self.last_ability = 0 # probably could go into Character class
    
    def try_to_register(self, ability: Ability) -> None:
        current_tick = ticks.get_current_tick()
        if current_tick - self.last_ability >= self.cool_down:
            self.register(ability)
            self.last_ability = current_tick

    def turn_sequence(self) -> None:
        for ability in self.get_pieces():
            ability.take_action()
        self.resolve_used_abilities()
    
    def resolve_used_abilities(self):
        self.pieces = [piece for piece in self.get_pieces() if not piece.is_attack_finished()]
