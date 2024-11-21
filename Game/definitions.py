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

class Direction(Enum):
    Up = (-1, 0)
    Down = (1, 0)
    Left = (0, -1)
    Right = (0, 1)

source_rarity_worth_map = {
    Rarity.COMMON: (1, 5),      
    Rarity.UNCOMMON: (6, 10),   
    Rarity.RARE: (11, 20),     
    Rarity.LEGENDARY: (21, 50)
}

source_rarity_weights = {
    Rarity.COMMON: 70,     
    Rarity.UNCOMMON: 20,  
    Rarity.RARE: 9,       
    Rarity.LEGENDARY: 1   # 1% chance
}