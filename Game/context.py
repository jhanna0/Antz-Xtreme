# Objects
from Game.board import Board
from Game.events import Events
from Pieces.player import Player
from Pieces.piece import Piece

# Managers
from Managers.machine_manager import MachineManager
from Managers.npc_manager import NPCManager
from Managers.shop_manager import ShopManager
from Managers.source_manager import SourceManager
from Managers.ability_manager import AbilityManager
from Game.generate import Generator

from typing import List

class GameContext:
    """
        Really just a way to hold a bunch of game data. A helper class to Game.
    """
    def __init__(
        self,
        player: Player,
        board: Board,
        abilities: AbilityManager,
        npcs: NPCManager,
        sources: SourceManager,
        machines: MachineManager,
        shops: ShopManager,
        generator: Generator,
        events: Events
    ):
        self.player: Player = player
        self.board: Board = board
        self.abilities: AbilityManager = abilities
        self.npcs: NPCManager = npcs
        self.sources: SourceManager = sources
        self.machines: MachineManager = machines
        self.shops: ShopManager = shops
        self.generator: Generator = generator
        self.events: Events = events

        self.all_objects: List[Piece] = []

    # any new pieces that need rendering go here
    # could make a registration method
    def _update_all_objects(self) -> None:
        """
        The list of content displayed on the board.
        Determines render order (smaller index takes priority).
        """
        self.all_objects = [
            *self.abilities.get_pieces(),
            self.player,
            *self.npcs.get_pieces(),
            *self.sources.get_pieces(),
            *self.machines.get_pieces(),
            *self.shops.get_pieces()
        ]

    def get_all_objects(self) -> List[Piece]:
        """
        Return the current list of all game objects. (Pass this to board to render each turn)
        """
        self._update_all_objects()
        return self.all_objects
