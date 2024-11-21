from typing import Dict, List, Tuple, TypeVar, Generic, Optional
from Pieces.piece import Piece


T = TypeVar("T", bound=Piece)  # Constrain T to subclasses of Piece

class Manager(Generic[T]):
    def __init__(self):
        self.pieces: Dict[str, List[T]] = {}

    def register(self, piece: T) -> None:
        symbol: str = piece.get_symbol()
        if symbol not in self.pieces:
            self.pieces[symbol] = []
        self.pieces[symbol].append(piece)

    def get_pieces(self) -> Dict[str, List[T]]:
        return self.pieces

    def get_pieces_list(self) -> List[T]:
        return [piece for sublist in self.pieces.values() for piece in sublist]

    def get_piece_at_location(self, location: Tuple[int, int]) -> T | None:
        for piece in self.get_pieces_list():
            if piece.get_location() == location:
                return piece
        return None

    def get_nearest_piece(self, location: Tuple[int, int]) -> Optional[T]:
        return min(self.get_pieces_list(), key = lambda piece: piece.get_distance_from(location), default = None)
