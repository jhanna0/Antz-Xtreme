from typing import Set

from Pieces.ability import Ability
from Managers.manager import Manager
from Game.board import Board
from Game.broadcast import broadcast
from Pieces.character import Character

class AbilityManager(Manager[Ability]):
    def __init__(self, board: Board):
        super().__init__()
        self.board = board
        
    def register(self, ability: Ability, character: Character) -> None:
        if character.can_use_ability():
            super().register(ability)

    def turn_sequence(self) -> None:
        for ability in self.get_pieces():
            ability.take_action()
        self.resolve_used_abilities()
    
    def resolve_used_abilities(self):
        self.pieces = [piece for piece in self.get_pieces() if not piece.is_attack_finished()]
