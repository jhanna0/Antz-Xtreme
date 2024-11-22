
# Objects
from Game.board import Board
from Game.events import Events
from Pieces.player import Player
from Pieces.robot import MinerRobot
from Pieces.shop import Shop
from Pieces.machine import MoneyMachine

# Managers
from Managers.machine_manager import MachineManager
from Managers.npc_manager import NPCManager
from Managers.shop_manager import ShopManager
from Managers.source_manager import SourceManager
from Managers.ability_manager import AbilityManager
from Game.generate import Generator

# Control and View
from Game.display import Display
from Game.broadcast import broadcast
from Game.controller import Controller
from Game.tick import ticks
from Game.tutorial import Tutorial
from Game.definitions import Direction
from Pieces.ability import Projectile, Ultimate, Teleport, Ring, Conjure


class Game:
    def __init__(self):
        # Viewports and Movement
        self.board = Board(10, 20)
        self.controller = Controller()
        self.move_list = {"w": Direction.Up, "a": Direction.Left, "s": Direction.Down, "d": Direction.Right}
        self.directional_ability_list = {"i": Direction.Up, "j": Direction.Left, "k": Direction.Down, "l": Direction.Right}
        self.ultimate = ["q", "f", "v"]
        
        # Managers
        self.npcs = NPCManager()
        self.generator = Generator(self.board)
        self.sources = SourceManager(self.generator)
        self.machines = MachineManager()
        self.shops = ShopManager()
        self.abilities = AbilityManager(self.board)
        self.events = Events(self.sources)

        # Player
        self.player_icon = "~"
        self.player = Player(symbol = self.player_icon, location = self.generator.find_location_for_piece())

        # Display after inventory
        self.display = Display(self.board, self.player.inventory)

        # Register entities
        self.machines.register(MoneyMachine(symbol = "$", location = self.generator.find_location_for_piece(edge_preference=True)))
        # self.shops.register(Shop(piece_type = MinerRobot, location = self.generator.find_location_for_piece(edge_preference=True)))

        # Tutorial(self.player_icon).start()

    def _update_board(self):
        # if adding new type of pieces, add here
        # can make a registration method too
        # determines render order (smaller index take priority)
        self.all_objects = [
            *self.abilities.get_pieces(),
            self.player,
            *self.npcs.get_pieces(),
            *self.sources.get_pieces(),
            *self.machines.get_pieces(),
            *self.shops.get_pieces(),
        ]

        self.board.update_piece_position(self.all_objects)
        self.display.update_display()

    def player_move(self, key):
        if key in self.move_list:
            next_move = self.player.next_move(self.move_list[key])
            if self.board.validate_move(next_move) and self.player.validate_move(next_move):
                self.player.move(next_move)
        
        elif key in self.directional_ability_list:
            self.abilities.try_to_register(Projectile(
                location = self.player.get_location(),
                direction = self.directional_ability_list[key],
                board = self.board,
                affects = [self.npcs, self.sources])
            )
    
        elif key == "q":
            self.abilities.try_to_register(Ultimate(
                size = self.board.get_size(),
                affects = [self.npcs, self.sources]
            ))
        
        elif key == "f":
            self.abilities.try_to_register(
                Teleport(
                    target = self.player,
                    board_size = self.board.get_size()
                )
            )
        elif key == "v":
            self.abilities.try_to_register(
                Conjure(
                    location = self.player.get_location(),
                    npcs = self.npcs
                )
            )

    def _sub_tick_sequence(self):
        key = self.controller.process_latest_input()
        if key:
            self.player_move(key)
        
        self.abilities.update()
        self._update_board()

    # probably can make a player manager class but do we reallllly need to just to pass every object ever??
    def player_turn_sequence(self):
        source = self.sources.get_piece_at_location(self.player.get_location())
        if source:
            self.player.interact_with_source(source)

        machine = self.machines.get_piece_at_location(self.player.get_location())
        if machine:
            self.player.interact_with_machine(machine)

        shop = self.shops.get_piece_at_location(self.player.get_location())
        if shop:
            purchase = self.player.purchase_from_shop(shop)
            if purchase:
                self.npcs.register(purchase)

    def _full_tick_sequence(self):
        self.sources.update()
        self.player_turn_sequence()
        self.npcs.turn_sequence(self.sources, self.machines)
        self.events.trigger_event(self.board.get_size())
        self._update_board()

    # should we move to a true tick system where all actions have durations?
    def run(self):
        self.controller.start()

        # this is kind of turn based kind of tick based- probably can be improved
        # seems like it's kind of just sleeping between actions, but really we should be having actions take a certain amount of ticks?
        # I do like this because it blocks action
        while self.controller.running:
            sub_tick, tick = ticks.tick()
            if sub_tick:
                self._sub_tick_sequence()

            if tick:
                self._full_tick_sequence()

            ticks.wait_until_next_tick()


game = Game()
game.run()
