import time

class TickManager:
    def __init__(self, tick_rate: float, sub_tick_ratio: int = 3):
        self.tick_rate = tick_rate  # Full tick interval
        self.sub_tick_rate = tick_rate / sub_tick_ratio  # Sub-tick interval
        self.game_time = None
        self.last_full_tick_time = None
        self.last_sub_tick_time = None
        self.total_ticks = 0

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
            return True
        return False

    def update_game_time(self):
        self.game_time = time.time()

    def get_game_time(self):
        return self.game_time

    def get_total_ticks(self):
        return self.total_ticks
