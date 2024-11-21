from enum import Enum

class Type(Enum):
    Player = "Player"
    Character = "Character"
    Robot = "Robot"
    NPC = "NPC"

class NpcState(Enum):
    Idle = "Idle"
    Collect = "Collect"
    Sell = "Sell"

# probably move into own rarity master class
class Rarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    LEGENDARY = "Legendary"
