from npc import NPC

class MinerRobot(NPC):
    def __init__(self, name: str, location: Tuple[int, int] = (0, 0)):
        super().__init__(Type.Robot, name, symbol="*", location=location, state=State.Idle)
        self.add_inventory_type("@")  # Miner-specific inventory type