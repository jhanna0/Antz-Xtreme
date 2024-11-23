from typing import List, Tuple, TypeVar, Generic, Optional, Type

from Pieces.piece import Piece
# all managers will probably need Generate now

T = TypeVar("T", bound=Piece)  # Constrain T to subclasses of Piece

class Manager(Generic[T]):
    def __init__(self):
        self.type = T
        self.pieces: List[T] = []

    def register(self, piece: T) -> None:
        self.pieces.append(piece)

    def get_pieces(self) -> List[T]:
        return self.pieces

    def get_piece_at_location(self, location: Tuple[int, int]) -> Optional[T]:
        """Returns the first instance of a piece at that location"""
        for piece in self.get_pieces():
            if piece.get_location() == location:
                return piece
        return None

    def get_all_pieces_at_location(self, location: Tuple[int, int]) -> List[T]:
        """Returns all pieces at the given location."""
        return [piece for piece in self.get_pieces() if piece.get_location() == location]

    def get_nearest_piece(self, location: Tuple[int, int]) -> Optional[T]:
        return min(self.get_pieces(), key = lambda piece: piece.get_distance_from(location), default = None)

    def remove_piece(self, remove: Piece) -> None:
        """Removes a piece from self.pieces"""
        if remove in self.pieces:
            self.pieces.remove(remove)
