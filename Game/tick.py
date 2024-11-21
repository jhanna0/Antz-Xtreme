import time
from typing import Optional


class TickManager:
    _instance: Optional["TickManager"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, tick_rate: 0.4, sub_tick_ratio: int = 3):
        if not hasattr(self, "_initialized"):  # Prevent reinitialization
            self._initialized = True
            self.tick_rate = tick_rate  # Full tick interval
            self.sub_tick_rate = tick_rate / sub_tick_ratio  # Sub-tick interval
            self.game_time = None
            self.last_full_tick_time = None
            self.last_sub_tick_time = None
            self.total_ticks = 0
            self.total_sub_ticks = 0

    def start(self):
        """Initialize timing."""
        time_now = time.time()
        self.game_time = time_now
        self.last_full_tick_time = time_now
        self.last_sub_tick_time = time_now

    def is_full_tick(self) -> bool:
        """Check if a full tick has elapsed and update state if true."""
        self.update_game_time()
        if self.game_time - self.last_full_tick_time >= self.tick_rate:
            self.last_full_tick_time = self.game_time
            self.total_ticks += 1
            return True
        return False

    def is_sub_tick(self) -> bool:
        """Check if a sub-tick has elapsed and update state if true."""
        self.update_game_time()
        if self.game_time - self.last_sub_tick_time >= self.sub_tick_rate:
            self.last_sub_tick_time = self.game_time
            self.total_sub_ticks += 1
            return True
        return False

    def update_game_time(self):
        """Update the current game time."""
        self.game_time = time.time()

    def get_game_time(self) -> float:
        """Get the current game time."""
        return self.game_time

    def get_total_ticks(self) -> int:
        """Get the total number of full ticks."""
        return self.total_ticks

    def get_total_sub_ticks(self) -> int:
        """Get the total number of sub-ticks."""
        return self.total_sub_ticks

    def time_since_last_tick(self) -> float:
        """Get the elapsed time since the last full tick."""
        return self.game_time - self.last_full_tick_time

    def time_since_last_sub_tick(self) -> float:
        """Get the elapsed time since the last sub-tick."""
        return self.game_time - self.last_sub_tick_time

    def wait_until_next_tick(self):
        """Block execution until the next full tick."""
        while not self.is_full_tick():
            time.sleep(0.001)  # Sleep for a short duration to reduce CPU usage

ticks = TickManager()
