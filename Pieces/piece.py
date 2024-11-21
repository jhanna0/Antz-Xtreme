from typing import Tuple

class Piece():
    def __init__(self, location: Tuple[int, int] = (0, 0), symbol: str = "*", size: Tuple[int, int] = (1, 1)):
        self.location = location
        self.symbol = symbol
        self.size = size
    
    def set_location(self, location: Tuple[int, int]) -> None:
        self.location = location

    def get_location(self) -> Tuple[int, int]:
        return self.location

    def get_symbol(self) -> str:
        return self.symbol
    
    def get_size(self) -> Tuple[int, int]:
        return self.size
    
    def get_distance_from(self, location: Tuple[int, int]) -> Tuple[int, int]:
        diff_x = self.location[0] - location[0]
        diff_y = self.location[1] - location[1]
        return abs(diff_x), abs(diff_y)

    def get_type(self) -> str:
        return self.__class__.__name__
