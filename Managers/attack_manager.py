from Pieces.attack import Attack
from Managers.manager import Manager
from Game.board import Board
from Game.tick import ticks
from Managers.npc_manager import NPCManager

class AttackManager(Manager[Attack]):
    def __init__(self, board: Board, npcs: NPCManager):
        super().__init__()
        self.board = board
        self.npcs = npcs
        self.cool_down = 2
        self.last_attack = 0 # probably could go into Character class
    
    def try_to_register(self, attack: Attack) -> None:
        current_tick = ticks.get_current_tick()
        if current_tick - self.last_attack >= self.cool_down:
            self.register(attack)
            self.last_attack = current_tick

    def update(self) -> None:
        self.calculate_damage()
        self.pieces = [piece for piece in self.get_pieces() if piece.validate_next_turn(self.board)]
        for attack in self.get_pieces():
            attack.next_turn()
    
    def calculate_damage(self) -> None:
        remove_attacks = []
        for attack in self.get_pieces():
            npc = self.npcs.get_piece_at_location(attack.get_location())
            if npc:
                self.npcs.remove_piece(npc)
                remove_attacks.append(attack)
        
        self.pieces = [piece for piece in self.get_pieces() if piece not in remove_attacks]
