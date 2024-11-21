from Pieces.piece import Piece
from typing import Tuple, Type, Optional
from Game.tick import ticks
from Game.broadcast import broadcast

# at the moment shop will only sell Pieces, but, we should also have Item Shop
class Shop(Piece):
    def __init__(self, piece_type: Type[Piece], location: Tuple[int, int] = (9, 19), symbol: str = "!"):
        super().__init__(location, symbol)
        self.purchases = 0
        self.base_price = 5

        # singleton global tick manager
        self.ticks = ticks

        # Store the class type (blueprint) of the item we're selling
        self.item_type: Type[Piece] = piece_type

        self.last_purchase_tick = 0
        self.cooldown = 20

    def get_price(self) -> int:
        return int(((self.purchases + 1) + self.base_price) ** 1.5)
    
    # don't know if this is best way
    def purchase(self) -> Optional[Piece]:
        tick = self.ticks.get_current_tick()
        if (tick - self.last_purchase_tick) > self.cooldown:
            self.last_purchase_tick = tick
            self.purchases += 1

            # these are not type safe at the moment.. improve later
            item = self.item_type(f"QT-{self.purchases}")

            broadcast.announce(f"A {item.get_type()}, {item.name}, joins your team!")
            return item
        
        return None
    
    # def give_tick(self, tick: int):
        
    def get_item_type(self) -> Type[Piece]:
        return self.item_type
