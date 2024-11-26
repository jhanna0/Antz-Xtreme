from random import randint

from Game.tick import ticks
from Game.broadcast import broadcast
from Game.generate import Generator
from Game.definitions import Rarity, random_event_rate

class Events():
    """
        A manager to randomly generate events in the game!
    """
    def __init__(self, generator: Generator):
        self.events = 0
        self.last_event_time = 0
        self.generator = generator

    def random_event(self):
        """
            Random event at some probability.
        """

        rarity = Rarity.COMMON
        start, end = random_event_rate[rarity]

        current_tick = ticks.get_current_tick()

        if current_tick > 20 and self.events == 0: # first event happens early
            self.generator.create_random_source()
            self.events += 1
            self.last_event_time = current_tick

        elif (current_tick - self.last_event_time) >= randint(start, end): # Trigger an event every ~240 ticks
            self.generator.create_random_source()
            self.last_event_time = current_tick
            self.events += 1
