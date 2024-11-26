from typing import List, Callable
from Game.broadcast import broadcast
from Inventory.inventory import Inventory
from Pieces.ability import Teleport
from Game.context import GameContext
from Pieces.robot import MinerRobot
from Pieces.shop import Shop
from Pieces.machine import MoneyMachine

class Chapter:
    def __init__(self, name: str, objective: str):
        self.name: str = name
        self.objective: str = objective
        self.started = False
        self.complete = False

    def starting_action(self) -> None:
        self.started = True
        broadcast.announce(self.name)
        broadcast.announce(f"Objective: {self.objective}")

    def completion_condition(self) -> bool:
        raise NotImplementedError()

    def completion_action(self) -> None:
        raise NotImplementedError()

    def set_completed(self) -> None:
        self.complete = True

    def is_complete(self):
        return self.complete

class Chapter1(Chapter):
    def __init__(self, inventory: Inventory):
        super().__init__(name = "Chapter 1", objective = "Pick up single resource")
        self.inventory = inventory

    def completion_condition(self) -> bool:
        return len(self.inventory.get_items()) > 0

    def completion_action(self) -> None:
        broadcast.announce("You completed Chapter 1!")

class Chapter2(Chapter):
    def __init__(self, context: GameContext, kb_str: str, callback: Callable):
        super().__init__(name = "Chapter 2", objective = "Fill your inventory")
        self.context = context
        self.kb_str = kb_str
        self.callback = callback

    def _use_teleport(self):
        """
        Use the Teleport ability.
        """
        self.context.abilities.try_to_register(Teleport(
            target=self.context.player,
            board_size=self.context.board.get_size()
        ))

    def completion_condition(self):
        return self.context.player.inventory.is_inventory_full()

    def completion_action(self):
        broadcast.announce(f"Completed")
        self.callback(self.kb_str, self._use_teleport)
        broadcast.announce("You've learned to teleport!")
        broadcast.announce("Press 'f' to teleport in your last travel direction.")

class Story:
    """The "CD-ROM" for our Framework. Loads a game to be played."""
    def __init__(self, name: str):
        self.name = name
        self.chapters: List[Chapter] = []
        self.current_chapter_index = 0
        self.won: bool = False

    def start(self):
        broadcast.announce(self.name)

    def add_chapter(self, chapter: Chapter):
        self.chapters.append(chapter)

    def win_condition(self) -> bool:
        """
        Checks if the win condition has been met for all chapters.
        """
        return all(chapter.complete for chapter in self.chapters)

    def win(self):
        """
        Handles winning the story. This will only run once.
        """
        if not self.won:
            self.won = True
            broadcast.announce("You win!!")

    def every_turn(self):
        """
        Override this method for custom logic to be executed every turn.
        """
        pass

    def play(self):
        """
        Updates the story's state. Manages chapter progression and win logic.
        """
        if self.win_condition():
            self.win()
            return  # If the game is won, stop further updates

        if self.current_chapter_index < len(self.chapters):
            current_chapter = self.chapters[self.current_chapter_index]

            self.every_turn() # run these actions while playing

            if not current_chapter.started:
                current_chapter.starting_action()

            if current_chapter.completion_condition():
                current_chapter.set_completed()

            if current_chapter.is_complete():
                current_chapter.completion_action()
                self.current_chapter_index += 1

class AntzStory(Story):
    def __init__(self, context: GameContext, kb_func: callable):
        super().__init__(name = "Antz Extreme")
        self.context = context
        self.chapters: List[Chapter] = []
        self.current_chapter_index = 0

        self.add_chapter(
            Chapter1(
                inventory = self.context.player.inventory
            )
        )
        self.add_chapter(
            Chapter2(
                context = self.context,
                kb_str = "f",
                callback = kb_func
            )
        )
    
    def start(self):
        super().start()
        # Register entities
        self.context.machines.register(
            MoneyMachine(
                symbol = "$",
                location = self.context.generator.find_location_for_piece(edge_preference = True)
            )
        )
        self.context.shops.register(
            Shop(
                piece_type = MinerRobot,
                location = self.context.generator.find_location_for_piece(edge_preference=True)
            )
        )
    
    def every_turn(self):
        self.context.events.random_event()
