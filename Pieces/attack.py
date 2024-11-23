from typing import Tuple
from Pieces.piece import Piece
from Game.definitions import Direction
from Game.board import Board

class Attack(Piece):
    def __init__(self, location: Tuple[int, int], symbol: str = "*"):
        super().__init__(location, symbol)
    
    def validate_next_turn(self):
        raise NotImplementedError()
    
    def next_turn(self) -> None:
        raise NotImplementedError()

class Projectile(Attack):
    def __init__(self, location: Tuple[int, int], direction: Direction = Direction.Right):
        super().__init__(location)
        self.direction = direction.value
    
    def _next_move(self) -> Tuple[int, int]:
        x = self.location[0] + self.direction[0]
        y = self.location[1] + self.direction[1]
        return (x, y)

    # same method in player class -> could make a "movable" piece class. npc doesn't take this because we assume all their moves are valid
    def validate_next_turn(self, board: Board) -> bool:
        return board.validate_move(self._next_move())

    def next_turn(self) -> None:
        self.location = self._next_move()
