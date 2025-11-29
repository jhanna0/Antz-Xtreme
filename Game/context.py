# Objects
from Game.board import Board
from Game.events import Events
from Pieces.player import Player
from Pieces.piece import Piece

# Managers
from Managers.entity_manager import EntityManager
from Game.generate import Generator

from typing import List, Dict, Type, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from Pieces.npc import NPC
    from Pieces.source import Source
    from Pieces.machine import Machine
    from Pieces.shop import Shop
    from Pieces.ability import Ability

class GameContext:
    """
    Really just a way to hold a bunch of game data. A helper class to Game.
    """
    def __init__(
        self,
        board: Board,
        player: Optional[Player] = None,
        generator: Optional[Generator] = None,
        events: Optional[Events] = None
    ):
        self.player: Optional[Player] = player
        self.board: Board = board
        self.generator: Generator = generator
        self.events: Events = events
        
        self.entity_manager = EntityManager()
        self.all_objects: List[Piece] = []

    def register_entity(self, piece: Piece) -> None:
        self.entity_manager.register(piece)

    def get_entities(self, type_cls: Type[Piece]) -> List[Piece]:
        return self.entity_manager.get_pieces_of_type(type_cls)

    # Deprecated manager accessors - mapped to entity manager queries for compatibility
    # Ideally these should be removed and callsites updated
    # Note: These now return List[Piece] to avoid runtime imports, or could use forward refs
    
    def get_manager(self, name: str) -> Any:
        """Deprecated: Returns entity manager or specific query wrapper"""
        # Adapting old manager access pattern to new entity manager
        if name in ["npcs", "sources", "machines", "shops", "abilities"]:
            return self.entity_manager 
        return None

    # any new pieces that need rendering go here
    def _update_all_objects(self) -> None:
        """
        The list of content displayed on the board.
        """
        # Add player
        objects = [self.player] if self.player else []
        
        # Add all other entities from manager
        # We can rely on EntityManager to provide them. 
        # If specific order is needed, the Story or Renderer should handle it.
        # For now, we dump everything.
        objects.extend(self.entity_manager.get_pieces())
        
        self.all_objects = objects

    def get_all_objects(self) -> List[Piece]:
        """
        Return the current list of all game objects. (Pass this to board to render each turn)
        """
        self._update_all_objects()
        return self.all_objects
