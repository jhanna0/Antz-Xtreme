from manager import Manager

class ShopManager(Manager):
    def __init__(self):
        super().__init__()

    # not used right now, probably is better to be here than in player logic tbh
    # def calculate_player_interaction(self, player: Player, npcs: NPCManager):
    #     for shop in self.shops.values():
    #         if player.get_location() == shop.get_location():
    #             price = shop.get_price()
    #             if player.get_money() >= price:
    #                 if shop.purchase():
    #                     player.remove_money(price)
    #                     robot = MinerRobot("QT")
    #                     robot.add_inventory_type("@")
    #                     npcs.register("*", robot)
