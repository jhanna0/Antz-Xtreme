from typing import Set

from Pieces.attack import Attack
from Managers.manager import Manager
from Game.board import Board
from Game.tick import ticks
from Managers.npc_manager import NPCManager
from Managers.source_manager import SourceManager
from Game.broadcast import broadcast

class AttackManager(Manager[Attack]):
    def __init__(self, board: Board):
        super().__init__()
        self.board = board
        self.cool_down = 2 # probably could go into Character class
        self.last_attack = 0 # probably could go into Character class
    
    def try_to_register(self, attack: Attack) -> None:
        current_tick = ticks.get_current_tick()
        if current_tick - self.last_attack >= self.cool_down:
            self.register(attack)
            self.last_attack = current_tick

    def update(self, npcs: NPCManager, sources: SourceManager) -> None:
        self.calculate_damage(npcs, sources)
        self.clear_invalid_attacks()
        for attack in self.get_pieces():
            attack.next_turn()
    
    def calculate_damage(self, npcs: NPCManager, sources: SourceManager) -> None:
        # we could even have attack responsible for which managers to check (prevents projectile from removing source)
        for attack in self.get_pieces():
            for npc in attack.calculate_hits(npcs):
                npcs.remove_piece(npc)

            # make projectiles not affect sources later
            for source in attack.calculate_hits(sources):
                sources.remove_piece(source)

    def clear_invalid_attacks(self):
        self.pieces = [piece for piece in self.get_pieces() if piece.validate_next_turn()]
