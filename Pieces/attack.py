from typing import Tuple, List, Set
from Pieces.piece import Piece
from Game.definitions import Direction
from Game.board import Board
from Managers.manager import Manager
from Managers.npc_manager import NPCManager

class Attack(Piece):
    def __init__(self, location: Tuple[int, int], symbol: str = "*"):
        super().__init__(location, symbol)
    
    def validate_next_turn(self):
        raise NotImplementedError()
    
    def next_turn(self) -> None:
        raise NotImplementedError()

    # could pass in "affeced type" or something but separately is fine for now
    def calculate_hits(self, manager: Manager) -> List[Piece]:
        affect: Set = set()
        raise NotImplementedError()

class Projectile(Attack):
    def __init__(self, location: Tuple[int, int], direction: Direction = Direction.Right):
        super().__init__(location)
        self.direction = direction.value
    
    def _next_move(self) -> Tuple[int, int]:
        x = self.location[0] + self.direction[0]
        y = self.location[1] + self.direction[1]
        return (x, y)

    def calculate_hits(self, npcs: NPCManager) -> List[Piece]:
        return npcs.get_all_pieces_at_location(self.get_location())

    # same method in player class -> could make a "movable" piece class. npc doesn't take this because we assume all their moves are valid
    def validate_next_turn(self, board: Board) -> bool:
        return board.validate_move(self._next_move())

    def next_turn(self) -> None:
        self.location = self._next_move()

class Ultimate(Attack):
    def __init__(self):
        super().__init__((0, 0))
        self.used = False

    def validate_next_turn(self) -> bool:
        self.used = True
        return True

    def next_turn(self, everything: List) -> None:
        # destroy everything
        pass
