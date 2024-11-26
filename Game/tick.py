import time
from typing import Tuple


class TickManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, tick_rate: float = 0.25):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.current_tick = 0
            
            self.tick_rate = tick_rate
            self.last_tick_time = time.time()
            self.last_sub_tick_time = self.last_tick_time

    def check_game_loop_tick(self) -> Tuple[bool, bool]:
        current_time = time.time()
        is_full_tick = False

        if current_time - self.last_tick_time >= self.tick_rate:
            self.last_tick_time = current_time
            self.current_tick += 1
            is_full_tick = True

        return is_full_tick

    def get_current_tick(self) -> int:
        return self.current_tick

    def get_tick_difference(self, tick: int): # this is not really useful because most times we need to set tick to new tick
        return self.current_tick - tick

    def wait_until_next_tick(self) -> None:
        time.sleep(0.001) # supposedly helps with CPU rest

ticks = TickManager()
