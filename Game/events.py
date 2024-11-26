from random import randint

from Game.tick import ticks
from Managers.source_manager import SourceManager
from Game.broadcast import broadcast

class Events():
    """
        A manager to randomly generate events in the game!
    """
    def __init__(self, sources: SourceManager):
        self.events = 0
        self.last_event_time = 0

        self.sources = sources

    def create_random_source(self):
        current_tick = ticks.get_current_tick()

        if current_tick > 20 and self.events == 0: # first event happens early
            self.sources.create_random_source()
            self.events += 1
            self.last_event_time = current_tick

        elif (current_tick - self.last_event_time) >= randint(50, 100): # Trigger an event every ~240 ticks
            self.sources.create_random_source()
            self.last_event_time = current_tick
            self.events += 1
