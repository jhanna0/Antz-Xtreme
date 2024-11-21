import time


class TickManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, tick_rate: float = 0.4, sub_tick_ratio: int = 2):
        if not hasattr(self, "_initialized"):  # Prevent reinitialization
            self._initialized = True

            self.current_tick = 0
            self.tick_rate = tick_rate
            self.sub_tick_rate = tick_rate / sub_tick_ratio # subtick action get (sub_tick_ratio) actions per turn (2)

            self.game_time = None
            self.last_sub_tick_time = None
            self.last_tick_time = None

    def start(self):
        """Initialize timing."""
        time_now = time.time()
        self.game_time = time_now
        self.last_tick_time = time_now
        self.last_sub_tick_time = time_now

    def get_current_tick(self) -> int:
        return self.current_tick

    def is_sub_tick(self) -> bool:
        if self._time_since_last_sub_tick() >= self.sub_tick_rate:
            self.last_sub_tick_time = self.game_time
            return True
        return False

    def is_full_tick(self) -> bool:
        if self._time_since_last_tick() >= self.tick_rate:
            self.last_tick_time = self.game_time
            self.current_tick += 1
            return True
        return False

    def wait_until_next_tick(self) -> None:
            time.sleep(0.01)

    def _time_since_last_sub_tick(self) -> float:
        self._update_game_time()
        return self.game_time - self.last_sub_tick_time

    def _time_since_last_tick(self) -> float:
        self._update_game_time()
        return self.game_time - self.last_tick_time

    def _update_game_time(self) -> None:
        self.game_time = time.time()

ticks = TickManager()
