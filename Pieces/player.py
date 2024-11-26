from Pieces.character import Character
from Game.definitions import Direction
from typing import Tuple
from Game.broadcast import broadcast
from Game.bank import bank
from Managers.machine_manager import MachineManager
from Managers.source_manager import SourceManager
from Game.board import Board

class Player(Character):
    def __init__(self, name: str = "You", location: Tuple[int, int] = (0, 0), symbol: str = "~"):
        super().__init__(name, location, symbol)
        self.last_direction = Direction.Right

    def next_move(self, direction: Direction) -> Tuple[int, int]:
        """
        Determines the next position based on the given direction.
        """
        x = self.location[0] + direction.value[0]
        y = self.location[1] + direction.value[1]
        self.last_direction = direction
        return (x, y)

    def validate_move(self, move: Tuple[int, int]) -> bool:
        """
        Validates whether a move is within allowed constraints.
        """
        diff_x = move[0] - self.location[0]
        diff_y = move[1] - self.location[1]
        return abs(diff_x) + abs(diff_y) == 1

    def move_player(self, board: Board, direction: Direction) -> None:
        """
        Moves the player in the given direction. Called from key_bindings in Game.
        """
        next_move = self.next_move(direction)
        if board.validate_move(next_move) and self.validate_move(next_move):
            self.move(next_move)
