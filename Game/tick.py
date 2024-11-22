import time
from typing import Tuple


class TickManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, tick_rate: float = 0.4, sub_tick_ratio: int = 2):
        if not hasattr(self, "_initialized"):
            self._initialized = True

            self.tick_rate = tick_rate
            self.sub_tick_rate = tick_rate / sub_tick_ratio
            self.current_tick = 0
            self.last_tick_time = time.time()
            self.last_sub_tick_time = self.last_tick_time

    def tick(self) -> Tuple[bool, bool]:
        current_time = time.time()
        is_full_tick = False
        is_sub_tick = False

        if current_time - self.last_sub_tick_time >= self.sub_tick_rate:
            self.last_sub_tick_time = current_time
            is_sub_tick = True

        if current_time - self.last_tick_time >= self.tick_rate:
            self.last_tick_time = current_time
            self.current_tick += 1
            is_full_tick = True

        return is_sub_tick, is_full_tick

    def get_current_tick(self) -> int:
        return self.current_tick

    def wait_until_next_tick(self) -> None:
        time.sleep(0.001) # supposedly helps with CPU rest

ticks = TickManager()
