from typing import Tuple, Dict, List

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
    
    def get_board_size(self) -> Tuple[int, int]:
        return (self.rows, self.cols)
    
    def update_piece_position(self, pieces: Dict[str, List]):
        self.clear_board()
        for piece_name, piece_list in pieces.items():
            for piece in piece_list:
                row, col = piece.get_location()
                self.board[row][col] = piece_name

                if piece.get_type() == "Source":
                    self.board[row][col + 1] = str(piece.get_quantity())
    
    def validate_move(self, move: Tuple[int, int]):
        if not (0 <= move[0] < self.rows) or not (0 <= move[1] < self.cols):
            return False
        
        # also check if there's a piece already under us
        return True
