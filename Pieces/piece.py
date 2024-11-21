from typing import Tuple

class Piece():
    def __init__(self, location: Tuple[int, int] = (0,0), symbol: str = "*", size: Tuple[int, int] = (1, 1)):
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

    def get_type(self) -> str:
        return self.__class__.__name__
