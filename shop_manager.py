from board import Board
from shop import Shop
from typing import Dict
from characters import Player, MinerRobot
from npc_manager import NPCManager

class ShopManager:
    def __init__(self, board: Board):
        self.shops: Dict[str, Shop] = {}
        self.board = board

    def register(self, symbol: str, shop: Shop):
        self.shops[symbol] = shop
        self.board.update_piece_position(self.shops)

    def calculate_player_interaction(self, player: Player, npcs: NPCManager):
        for shop in self.shops.values():
            if player.get_location() == shop.get_location():
                price = shop.get_price()
                if player.get_money() >= price:
                    if shop.purchase():
                        player.remove_money(price)
                        robot = MinerRobot("QT")
                        robot.add_inventory_type("@")
                        npcs.register("*", robot)
