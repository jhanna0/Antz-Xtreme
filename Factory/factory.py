from typing import List, Callable

from Game.context import GameContext
from Pieces.ability import Teleport, Projectile, Ultimate, Conjure
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
                target = self.context.player,
                board_size = self.context.board.get_size()
            )
            self.context.abilities.register(ability)

        return teleport_action

    def directional_projectile(self, direction: str) -> Callable:
        """
        Creates and registers a Projectile ability in a specific direction.
        Returns a callable that can be invoked to activate the ability.
        """
        def projectile_action():
            ability = Projectile(
                location = self.context.player.get_location(),
                direction = direction,
                board = self.context.board,
                affects = [self.context.npcs, self.context.sources]
            )
            self.context.abilities.register(ability)

        return projectile_action

    def ultimate_ability(self) -> Callable:
        """
        Creates and registers an Ultimate ability.
        Returns a callable that can be invoked to activate the ability.
        """
        def ultimate_action():
            ability = Ultimate(
                size = self.context.board.get_size(),
                affects = [self.context.npcs, self.context.sources]
            )
            self.context.abilities.register(ability)

        return ultimate_action

    def conjure_ability(self) -> Callable:
        """
        Creates and registers a Conjure ability.
        Returns a callable that can be invoked to activate the ability.
        """
        def conjure_action():
            ability = Conjure(
                location = self.context.player.get_location(),
                npcs = self.context.npcs,
                sources = self.context.sources,
                machines = self.context.machines
            )
            self.context.abilities.register(ability)

        return conjure_action
