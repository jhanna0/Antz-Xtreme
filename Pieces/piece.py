from typing import Tuple
from uuid import uuid4

class Piece():
    def __init__(self, location: Tuple[int, int] = (0, 0), symbol: str = "*", size: Tuple[int, int] = (1, 1)):
        self.location = location
        self.symbol = symbol
        self.size = size
        self.id = uuid4()
    
    def set_location(self, location: Tuple[int, int]) -> None:
        self.location = location

    def get_location(self) -> Tuple[int, int]:
        return self.location

    def get_symbol(self) -> str:
        return self.symbol
    
    def get_footprint(self) -> str:
        """Returns what piece should look like on the board."""
        height, width = self.size
        row = f"{self.symbol}" * width
        return "\n".join([row] * height)

    def get_size(self) -> Tuple[int, int]:
        return self.size

    def set_size(self, size: Tuple[int, int]) -> None:
        self.size = size
    
    def get_distance_from(self, location: Tuple[int, int]) -> Tuple[int, int]:
        diff_x = self.location[0] - location[0]
        diff_y = self.location[1] - location[1]
        return abs(diff_x), abs(diff_y)

    def get_type(self) -> str:
        return self.__class__.__name__
    
    def get_id(self):
        return self.id

