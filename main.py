from typing import List

# Objects
from Game.board import Board
from Game.events import Events
from Pieces.player import Player
from Pieces.robot import MinerRobot
from Pieces.shop import Shop
from Pieces.machine import MoneyMachine
from Game.story import Chapter, Chapter1, Chapter2
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

class GameContext:
    def __init__(
        self,
        player: Player,
        board: Board,
        abilities: AbilityManager,
        sources: SourceManager,
        npcs: NPCManager,
        machines: MachineManager,
        shops: ShopManager,
        generator: Generator,
        events: Events
    ):
        self.player = player
        self.board = board
        self.abilities = abilities
        self.sources = sources
        self.npcs = npcs
        self.machines = machines
        self.shops = shops
        self.generator = generator
        self.events = events

class Game:
    def __init__(self):
        # Initialize viewports and movement
        self.controller = Controller()

        # Movement and abilities
        self.move_list = {"w": Direction.Up, "a": Direction.Left, "s": Direction.Down, "d": Direction.Right}
        self.directional_ability_list = {"i": Direction.Up, "j": Direction.Left, "k": Direction.Down, "l": Direction.Right}
        self.key_bindings = {}

        # Core managers
        self.board = Board(10, 20)
        self.npcs = NPCManager()
        self.generator = Generator(self.board)
        self.sources = SourceManager(self.generator)
        self.machines = MachineManager()
        self.shops = ShopManager()
        self.abilities = AbilityManager(self.board)
        self.events = Events(self.sources)

        # Player
        self.player = Player(symbol="~", location=self.generator.find_location_for_piece())

        # Display
        self.display = Display(self.board, self.player.inventory)

        # Register entities
        self.machines.register(MoneyMachine(symbol="$", location=self.generator.find_location_for_piece(edge_preference=True)))
        self.shops.register(Shop(piece_type=MinerRobot, location=self.generator.find_location_for_piece(edge_preference=True)))

        # Initialize chapters
        self.initialize_chapters()

        # Key bindings
        self._register_default_keybindings()

        # Game context
        self.context = GameContext(
            player=self.player,
            board=self.board,
            abilities=self.abilities,
            sources=self.sources,
            npcs=self.npcs,
            machines=self.machines,
            shops=self.shops,
            generator=self.generator,
            events=self.events
        )
    
    def _register_keybinding(self, key: str, action: callable):
        self.key_bindings[key] = action

    def _register_default_keybindings(self):
        # default movement keys that should be used for every Game
        for key, direction in self.move_list.items():
            self._register_keybinding(key, lambda direction=direction: self._move_player(direction))

    def initialize_chapters(self):
        self.chapter_index = 0
        self.chapters: List[Chapter] = []
        # self.chapters.append(Chapter1(self.player.inventory, "f", self._register_keybinding))
        self.chapters.append(Chapter2(self.context, "f", self._register_keybinding))

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

    def _move_player(self, direction: Direction):
        next_move = self.player.next_move(direction)
        if self.board.validate_move(next_move) and self.player.validate_move(next_move):
            self.player.move(next_move)

    def handle_input(self):
        key = self.controller.process_latest_input()
        action = self.key_bindings.get(key)

        if action:
            action()  # Call the corresponding function

    # def player_move(self, key):
    #     if key in self.move_list:
    #         next_move = self.player.next_move(self.move_list[key])
    #         if self.board.validate_move(next_move) and self.player.validate_move(next_move):
    #             self.player.move(next_move)
        
    #     elif key in self.directional_ability_list:
    #         self.abilities.try_to_register(Projectile(
    #             location = self.player.get_location(),
    #             direction = self.directional_ability_list[key],
    #             board = self.board,
    #             affects = [self.npcs, self.sources])
    #         )
    
    #     elif key == "q":
    #         self.abilities.try_to_register(Ultimate(
    #             size = self.board.get_size(),
    #             affects = [self.npcs, self.sources]
    #         ))
        
    #     elif key == "f":
    #         self.abilities.try_to_register(
    #             Teleport(
    #                 target = self.player,
    #                 board_size = self.board.get_size()
    #             )
    #         )
    #     elif key == "v":
    #         self.abilities.try_to_register(
    #             Conjure(
    #                 location = self.player.get_location(),
    #                 npcs = self.npcs
    #             )
    #         )

    def _sub_tick_sequence(self):
        self.handle_input()
        self.abilities.turn_sequence()
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
        self.sources.turn_sequence()
        self.player_turn_sequence()
        self.npcs.turn_sequence(self.sources, self.machines)
        self.events.turn_sequence()
        self._update_board()

    def progress_story(self):
        if self.chapter_index < len(self.chapters):
            current_chapter = self.chapters[self.chapter_index]

            if not current_chapter.started:
                current_chapter.starting_action()

            # Delegate state transitions to the chapter
            if current_chapter.completion_condition():
                current_chapter.set_completed()

            # If the chapter is complete, move to the next one
            if current_chapter.is_complete():
                current_chapter.completion_action()
                self.chapter_index += 1

    def win_condition(self) -> bool:
        return all(chapter.complete for chapter in self.chapters)

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

            self.progress_story()
            if self.win_condition():
                pass
                # self.controller.stop()

            ticks.wait_until_next_tick()

game = Game()
game.run()
