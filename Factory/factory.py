from typing import List, Callable

from Game.context import GameContext
from Pieces.ability import Teleport
from Game.broadcast import broadcast

class Factory:
    """Cleaner solution to high dependency methods"""
    def __init__(self):
        pass

class AbilityFactory(Factory):
    def __init__(self, context: GameContext):
        self.context = context

    def player_teleport(self) -> Callable:
        """
        Creates and registers a Teleport ability for the player.
        Returns a callable that can be invoked to activate the ability.
        """
        def teleport_action():
            ability = Teleport(
                target=self.context.player,
                board_size=self.context.board.get_size()
            )
            self.context.abilities.register(ability)
        
        return teleport_action
