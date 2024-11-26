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

class Rarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    LEGENDARY = "Legendary"

class Speed(Enum):
    LONG = 20
    SLOW = 8
    NORMAL = 4
    INSTANT = 0

class Direction(Enum):
    Up = (-1, 0)
    Down = (1, 0)
    Left = (0, -1)
    Right = (0, 1)

# source
source_rarity_weights = {
    Rarity.COMMON: 70,     
    Rarity.UNCOMMON: 20,  
    Rarity.RARE: 9,       
    Rarity.LEGENDARY: 1   # 1% chance
}

source_worth_map = {
    Rarity.COMMON: (1, 5),      
    Rarity.UNCOMMON: (6, 10),   
    Rarity.RARE: (11, 20),     
    Rarity.LEGENDARY: (21, 50)
}

source_creation_rate = {
    Rarity.COMMON: (30, 40),      
    Rarity.UNCOMMON: (30, 20),   
    Rarity.RARE: (10, 20),     
    Rarity.LEGENDARY: (1, 10)
}

random_event_rate = {
    Rarity.COMMON: (50, 100),      
    Rarity.UNCOMMON: (100, 150),   
    Rarity.RARE: (150, 200),     
    Rarity.LEGENDARY: (200, 250)
}

superscript_mapping = {
    0: chr(0x2070),  # ⁰
    1: chr(0x00B9),  # ¹
    2: chr(0x00B2),  # ²
    3: chr(0x00B3),  # ³
    4: chr(0x2074),  # ⁴
    5: chr(0x2075),  # ⁵
    6: chr(0x2076),  # ⁶
    7: chr(0x2077),  # ⁷
    8: chr(0x2078),  # ⁸
    9: chr(0x2079)   # ⁹
}

