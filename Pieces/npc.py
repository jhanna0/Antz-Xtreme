from typing import Tuple, Callable, Optional, TYPE_CHECKING

from Pieces.character import Character
from Game.definitions import NpcState, Speed
from Game.tick import ticks

if TYPE_CHECKING:
    from Game.context import GameContext

def check_set_tick(func: Callable) -> Callable:
    """A pseudo way to make actions require X ticks to use. Should be moved into an Action base class."""
    def wrapper(self, *args, **kwargs):
        if ticks.get_tick_difference(self.start_tick) < self.speed:
            return None
        self.start_tick = ticks.get_current_tick()
        return func(self, *args, **kwargs)
    return wrapper

# give despawn time
class NPC(Character):
    def __init__(self, context: 'GameContext', name: str, location: Tuple[int, int], symbol: str):
        super().__init__(name, location, symbol)
        self.context = context
        self.destination: Tuple[int, int] = location
        self.state: NpcState = NpcState.Idle
        
        # Resolve dependencies via context
        # Dependencies are now resolved dynamically via self.context
        
        self.speed = Speed.NORMAL.value
        self.start_tick = ticks.get_current_tick()

    @check_set_tick
    def move(self) -> None:
        """
        Moves the NPC one step closer to its destination.
        """
        x, y = self.location
        dest_x, dest_y = self.destination

        # Vertical then horizontal movement
        if x != dest_x:
            x += 1 if dest_x > x else -1
        elif y != dest_y:
            y += 1 if dest_y > y else -1

        self.location = (x, y)

    def update(self) -> None:
        super().update() # Character.update() (interactions)
        self.decide_next_action()
        self.move()

    def decide_next_action(self) -> None:
        """
        Decides the NPC's next destination or action based on game state.
        """
        raise NotImplementedError()

    def at_destination(self) -> bool:
        """
        Checks if the NPC has reached its destination.
        """
        return self.location == self.destination

    def set_destination(self, destination: Tuple[int, int]) -> None:
        """
        Sets the NPC's next destination.
        """
        self.destination = destination
