from typing import Tuple, TYPE_CHECKING
from Pieces.piece import Piece

if TYPE_CHECKING:
    from Game.context import GameContext

class Ability(Piece):
    """
    Base class for all abilities.
    Abilities are transient pieces that exist on the board for a duration or until an action is complete.
    """
    def __init__(self, location: Tuple[int, int], context: 'GameContext', symbol: str = "*"):
        super().__init__(location, symbol)
        self.context = context
    
    def take_action(self) -> None:
        """
        Execute the ability's effect. Called every update.
        """
        raise NotImplementedError()

    def is_complete(self) -> bool:
        """
        Check if the ability has completed its effect/duration.
        """
        raise NotImplementedError()

    def update(self) -> None:
        """
        Standard entity update cycle.
        """
        self.take_action()

    def is_expired(self) -> bool:
        """
        Check if the entity should be removed from the game.
        """
        return self.is_complete()

