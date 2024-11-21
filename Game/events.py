from typing import Tuple
from random import randint

from Game.tick import ticks
from Managers.source_manager import SourceManager


class Events():
    def __init__(self, sources: SourceManager):
        self.events = 0
        self.last_event_time = 0

        self.sources = sources

    def trigger_event(self, board_size: Tuple[int, int]):
        total_ticks = ticks.get_total_ticks()

        if total_ticks > 20 and self.events == 0: # first event happens early
            self.sources.create_random_source(board_size)
            self.events += 1
            self.last_event_time = total_ticks

        elif (total_ticks - self.last_event_time) >= randint(180, 300): # Trigger an event every ~240 ticks
            self.sources.create_random_source(board_size)
            self.last_event_time = total_ticks
            self.events += 1
