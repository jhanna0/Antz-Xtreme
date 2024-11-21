from typing import Dict, List, Tuple
from Pieces.piece import Piece

class Manager:
    def __init__(self):
        self.pieces: Dict[str, List[Piece]] = {}

    def register(self, piece: Piece) -> None:
        symbol: str = piece.get_symbol()
        if symbol not in self.pieces:
            self.pieces[symbol] = []

        self.pieces[symbol].append(piece)

    def get_pieces(self) -> Dict[str, List[Piece]]:
        return self.pieces
    
    def get_piece_array(self) -> List[Piece]:
        return [piece for sublist in self.pieces.values() for piece in sublist]
    
    def get_piece_at_location(self, location: Tuple[int, int]) -> Tuple | None:
        for piece in self.get_piece_array():
            if piece.get_location() == location:
                return piece
        return None
