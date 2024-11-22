import time
from typing import List

from Game.broadcast import broadcast

class Tutorial():
    def __init__(self, icon: str):
        self.icon = icon
        self.intro_msgs: List[str] = [
            f"You are {self.icon}.",
            f"Mine resources. Sell resources at $.",
            f"Purchase upgrades at !."
        ]
    
    def start(self):
        time.sleep(0.5)
        for msg in self.intro_msgs:
            broadcast.announce(msg)
            time.sleep(2)
