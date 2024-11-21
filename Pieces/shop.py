from Pieces.piece import Piece
from typing import Tuple, Type

# at the moment shop will only sell Pieces, but, we should also have Item Shop
class Shop(Piece):
    def __init__(self, piece_type: Type[Piece], location: Tuple[int, int] = (9, 19), symbol: str = "!"):
        super().__init__(location, symbol)
        self.purchases = 0
        self.base_price = 5

        # Store the class type (blueprint) of the item we're selling
        self.item_type: Type[Piece] = piece_type

        self.last_purchase_tick = 0
        self.cooldown = 20

    def get_price(self) -> int:
        return int(((self.purchases + 1) + self.base_price) ** 1.5)
    
    # mmhhh don't know if this is best way
    def purchase(self, tick: int) -> Piece | None:
        """Handles the purchase and returns a new instance of the item."""
        if (tick - self.last_purchase_tick) > self.cooldown:
            self.last_purchase_tick = tick
            self.purchases += 1

            return self.item_type(f"Bot-{self.purchases}")
        
        return None
    
    # def give_tick(self, tick: int):
        
    def get_item_type(self) -> Type[Piece]:
        return self.item_type
