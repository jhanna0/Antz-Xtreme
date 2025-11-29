from typing import List, Tuple, Optional, Type
from Pieces.piece import Piece
from Game.signals import signals, SignalType

class EntityManager:
    """
    The core container for all game entities. Replaces specific managers.
    """
    def __init__(self):
        self.entities: List[Piece] = []
        # We could add a spatial index here for optimization later
        signals.subscribe(SignalType.INTERACTION_QUERY, self._handle_interaction_query)

    def register(self, piece: Piece) -> None:
        """Add a new piece to the world."""
        self.entities.append(piece)

    def update(self) -> None:
        """
        Update all entities in the world.
        This is the core game loop for entities.
        """
        remove_pieces: List[Piece] = []
        
        # Snapshot list to safely modify during iteration
        current_entities = list(self.entities)
        
        for piece in current_entities:
            piece.update()
            if piece.is_expired():
                remove_pieces.append(piece)
        
        for piece in remove_pieces:
            self.remove_piece(piece)

    def remove_piece(self, piece: Piece) -> None:
        """Remove a piece from the world."""
        if piece in self.entities:
            self.entities.remove(piece)
            signals.emit(SignalType.PIECE_REMOVED, {"piece": piece, "manager": self})

    def _handle_interaction_query(self, signal):
        """
        Handle generic interaction queries from characters.
        Dispatches specific signals based on what is found at the location.
        """
        piece = signal.data.get("piece")
        location = signal.data.get("location")
        
        # Find other pieces at this location
        targets = self.get_all_pieces_at_location(location)
        
        for target in targets:
            if target == piece:
                continue
                
            # Dispatch specific interaction signals based on type
            # using class name to avoid circular imports
            type_name = target.__class__.__name__
            
            if type_name == "Source":
                signals.emit(SignalType.INTERACT_WITH_SOURCE, {
                    "source": target,
                    "target": piece
                })
            elif "Machine" in type_name: # MoneyMachine, etc.
                signals.emit(SignalType.INTERACT_WITH_MACHINE, {
                    "machine": target,
                    "target": piece
                })

    # Queries
    def get_pieces(self) -> List[Piece]:
        """Return all pieces."""
        return list(self.entities)

    def get_pieces_of_type(self, type_cls: Type[Piece]) -> List[Piece]:
        """Return all pieces of a specific type (or subtype)."""
        return [p for p in self.entities if isinstance(p, type_cls)]

    def get_piece_at_location(self, location: Tuple[int, int]) -> Optional[Piece]:
        """Returns the first instance of a piece at that location."""
        for piece in self.entities:
            if piece.get_location() == location:
                return piece
        return None
    
    def get_all_pieces_at_location(self, location: Tuple[int, int]) -> List[Piece]:
        """Returns all pieces at the given location."""
        return [piece for piece in self.entities if piece.get_location() == location]

    def get_nearest_piece(self, location: Tuple[int, int], type_filter: Optional[Type[Piece]] = None) -> Optional[Piece]:
        """Find the nearest piece, optionally filtered by type."""
        candidates = self.entities
        if type_filter:
            candidates = [p for p in self.entities if isinstance(p, type_filter)]
            
        if not candidates:
            return None
            
        return min(candidates, key=lambda piece: piece.get_distance_from(location))

