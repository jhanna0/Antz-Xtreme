from Pieces.character import Character

class Player(Character):

    def __init__(self, name: str, symbol: str):
        super().__init__(Type.Player, name=name, symbol=symbol)
        self.money = 0      
    
    def next_move(self, direction: Direction) -> Tuple[int, int]:
        x = self.location[0] + direction.value[0]
        y = self.location[1] + direction.value[1]
        return (x, y)

    def validate_move(self, move: Tuple[int, int]):
        diff_x = move[0] - self.location[0]
        diff_y = move[1] - self.location[1]

        # we can only move one square at a time
        return abs(diff_x) + abs(diff_y) == 1

    def move(self, move: Tuple[int, int]):
        self.location = move

    def get_money(self):
        return self.money

    def add_money(self, amount):
        if amount > 0:
            self.money += amount

    def remove_money(self, amount):
        if amount > 0:
            self.money -= amount

    # can probably make this better and merged with NPC interaction logic
    # this is so bad how NPC manager is cyclically referenced.. fix. probably outside of loop
    def calculate_interactions(self, sources: SourceManager, machines: MachineManager):
        for source in sources.get_piece_array():
            if self.get_location() == source.get_location():
                item = source.take()
                if item:
                    self.add_to_inventory(item)
                    return

        for machine in machines.get_piece_array():
            if self.get_location() == machine.get_location():
                if self.any_in_inventory():
                    item = self.get_inventory().pop()
                    self.add_money(machine.convert(item))
                    BroadCast().announce(f"You sold {item.get_symbol()} for ${item.get_worth()}")
                    return
    
    def purchase_from_shop(self, shops: ShopManager, ticks: int) -> Tuple[bool, str, str]:
        """
        Attempt to purchase from a shop. Return a tuple indicating success,
        the shop symbol, and the item type purchased.
        """
        for shop in shops.get_piece_array():
            if self.get_location() == shop.get_location():
                price = shop.get_price()

                if self.get_money() >= price:
                    if shop.purchase(ticks):
                        self.remove_money(price)
                        return True, shop.get_item_symbol(), shop.get_item()
        
        return False, "", ""
