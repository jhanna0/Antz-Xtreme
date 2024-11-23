from typing import Tuple, List
from Pieces.piece import Piece
from Game.broadcast import broadcast

class Board():
    def __init__(self, rows: int = 3, cols: int = 9):
        self.rows = rows
        self.cols = cols
        self.board_symbol = "_"
        self.clear_board()
    
    def clear_board(self):
        self.board = [[self.board_symbol for _ in range(self.cols)] for _ in range(self.rows)]

    def get_board(self):
        return self.board
    
    # these need to be dynamic in case we make board grow
    def get_size(self) -> Tuple[int, int]:
        """Returns (height/rows, width/columns)"""
        return (self.rows, self.cols)
    
    def update_piece_position(self, pieces: List[Piece]):
        self.clear_board()
        for piece in pieces:
            self.place(piece)
            # if self.can_place(piece.get_size(), piece.get_location()):
            #     # broadcast.announce(f"placing {piece.get_symbol()}, {piece.get_location()}")
            #     self.place(piece)
            
            # else:
            #     # need to handle invalid pieces more gracefully
            #     broadcast.announce(f"can't place {piece.get_symbol()}, {piece.get_location()}")

    # ok kind of working. a couple problems:
    # 1. we have to be on exact location to interact with the object
    # 1.5 but we touch any part of footprint and it stops displaying the piece
    # 2. can only spawn one object at a time now
    # 3. validate_move only checks the pieces central location as well
    # 4. we use piece_size and footprint interchangebly but they could be different
    def can_place(self, piece_size: Tuple[int, int], location: Tuple[int, int]) -> bool:
        width, height = piece_size
        for dy in range(width):
            for dx in range(height):
                x, y = location[0] + dx, location[1] + dy

                # Check if within board bounds
                if not (0 <= x < self.rows and 0 <= y < self.cols):
                    return False
                
                # Check if the location is available
                if self.get_board()[x][y] != self.board_symbol:
                    return False
        return True

    def place(self, piece: Piece) -> None:
        """Place a piece on the board. Only supports horizontal at the moment."""
        # to flip to placing horizontally, we just increment (+ dy) over cols instead of rows
        footprint = piece.get_footprint().split("\n")
        height, width = piece.get_size()
        location = piece.get_location()
        broadcast.announce(f"{width} {height} {footprint} {location} {piece.get_type()} {self.get_size()}")
        for dy in range(height):
            for dx in range(width):
                self.board[location[0] + dy][location[1] + dx] = footprint[dy][dx]

    # update this to check footprint
    def validate_move(self, move: Tuple[int, int]):
        if not (0 <= move[0] < self.rows) or not (0 <= move[1] < self.cols):
            return False
        
        # also check if there's a piece already under us
        return True
