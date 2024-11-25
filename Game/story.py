from typing import List, Callable
from Game.broadcast import broadcast
from Inventory.inventory import Inventory
from Game.bank import Bank
from Pieces.ability import Teleport
from Managers.ability_manager import AbilityManager
from Pieces.player import Player
from Game.board import Board
from main import GameContext

class Chapter:
    def __init__(self):
        self.name: str = ''
        self.objective: str = ''
        self.started = False
        self.complete = False

    def starting_action(self):
        raise NotImplementedError()

    def completion_condition(self):
        raise NotImplementedError()

    def completion_action(self):
        raise NotImplementedError()

    def set_completed(self) -> None:
        self.complete = True

    def is_complete(self):
        return self.complete

class Chapter1(Chapter):
    def __init__(self, inventory: Inventory):
        self.name = "Chapter 1"
        self.objective: str = "Fill your inventory with resources"
        self.complete = False
        self.started = False
        self.inventory = inventory

    def starting_action(self):
        self.started = True
        broadcast.announce("Chapter 1: Learning the Ropes")
        broadcast.announce("Objective: ", self.objective)

    def completion_condition(self):
        return self.inventory.is_inventory_full()

    def completion_action(self):
        if self.complete:
            broadcast.announce("You completed Chapter 1!")

class Chapter2(Chapter):
    def __init__(self, context: GameContext, kb_str: str, callback: Callable):
        self.name = "Chapter 2"
        self.objective: str = "Collect $200"
        self.complete = False
        self.started = False
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

    def starting_action(self):
        self.started = True
        broadcast.announce("Chapter 2: Your first ability")
        broadcast.announce(f"Objective: {self.objective}")

    def completion_condition(self):
        return self.context.player.inventory.is_inventory_full()

    def completion_action(self):
        broadcast.announce(f"Completed")
        self.callback(self.kb_str, self._use_teleport)
        broadcast.announce("You've learned to teleport!")
        broadcast.announce("Press 'f' to teleport in your last travel direction")

class Story:
    """The "CD-ROM" for our Framework. Loads a game to be played."""
    def __init__(self, name: str):
        self.name = name
        self.chapters: List[Chapter] = []
        self.current_chapter_index = 0

    def add_chapter(self, chapter: Chapter):
        self.chapters.append(chapter)

    def win_condition(self) -> bool:
        return all(chapter.complete for chapter in self.chapters)

    def progress(self):
        if self.current_chapter_index < len(self.chapters):
            current_chapter = self.chapters[self.current_chapter_index]
            
            if not current_chapter.complete:
                current_chapter.progress()
            else:
                current_chapter.completion_action()
                self.current_chapter_index += 1

            if self.current_chapter_index < len(self.chapters):
                next_chapter = self.chapters[self.current_chapter_index]
                next_chapter.starting_action()
        else:
            print("Story complete!")

