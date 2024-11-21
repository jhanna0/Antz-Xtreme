from Pieces.character import Character
from Game.definitions import Direction
from Pieces.shop import Shop
from Pieces.piece import Piece # is this cyclical?
from typing import Tuple, Optional
from Game.broadcast import broadcast
from Game.bank import bank

class Player(Character):

    def __init__(self, name: str = "You", location: Tuple[int, int] = (0,0), symbol: str = "~"):
        super().__init__(name, location, symbol)
    
    def next_move(self, direction: Direction) -> Tuple[int, int]:
        x = self.location[0] + direction.value[0]
        y = self.location[1] + direction.value[1]
        return (x, y)

    def validate_move(self, move: Tuple[int, int]) -> bool:
        diff_x = move[0] - self.location[0]
        diff_y = move[1] - self.location[1]

        # we can only move one square at a time
        return abs(diff_x) + abs(diff_y) == 1

    def move(self, move: Tuple[int, int]) -> None:
        self.location = move
    
    # this is janky and will probably be moved somewhere else, maybe shop manager
    # probably don't need to pass ticks
    def purchase_from_shop(self, shop: Shop) -> Optional[Piece]:
        purchase = None
        price = shop.get_price()
        if bank.enough_money(price):
            # added a cooldown to purchasing to avoid duplicate purchases
            purchase = shop.purchase()
            if purchase:
                bank.remove_money(price)        
        else:
            broadcast.announce(f"Not enough money! Price: ${price}")
        
        return purchase
