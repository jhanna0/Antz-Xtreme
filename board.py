from typing import Tuple

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
    
    def get_board_size(self):
        return (self.rows, self.cols)
    
    def update_piece_position(self, pieces) -> bool:
        original_board = self.board.copy()
        self.clear_board()
        for piece_name, piece in pieces.items():
            row, col = piece.get_location()

            self.board[row][col] = piece_name

            if piece.get_type() == "Source":
                self.board[row][col + 1] = str(piece.get_quantity())
                    
        # is this logic working? only update display if changed
        return original_board != self.board
    
    def check_validate_move(self, piece_location: Tuple, new_location: Tuple):
        if not (0 <= new_location[0] < self.rows) or not (0 <= new_location[1] < self.cols):
            return False

        diff_x = new_location[0] - piece_location[0]
        diff_y = new_location[1] - piece_location[1]

        # also check if another piece is under us
        return abs(diff_x) + abs(diff_y) == 1

