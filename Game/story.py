from typing import List, Callable, Optional
from Game.broadcast import broadcast

class Chapter:
    def __init__(self, name: str, objective: str):
        self.name: str = name
        self.objective: str = objective
        self.started = False
        self.complete = False

    def starting_action(self) -> None:
        self.started = True

    def completion_condition(self) -> bool:
        raise NotImplementedError()

    def completion_action(self) -> None:
        raise NotImplementedError()

    def set_completed(self) -> None:
        self.complete = True

    def is_complete(self):
        return self.complete
    
    def get_objective(self) -> str:
        return self.objective

    def get_chapter_name(self) -> str:
        return self.name

class Story:
    """The "CD-ROM" for our Framework. Loads a game to be played."""
    def __init__(self, name: str):
        self.name = name
        self.chapters: List[Chapter] = []
        self.current_chapter_index = 0
        self.won: bool = False

    def start(self):
        # broadcast.announce(self.name)
        pass

    def setup(self, game):
        """
        Configure the game instance. Register managers, etc.
        Override this to register custom managers.
        """
        pass

    def add_chapter(self, chapter: Chapter):
        self.chapters.append(chapter)
    
    def get_story_name(self) -> str:
        return self.name
    
    def get_chapter_name(self) -> str:
        if self.won:
            return "You Win!"

        elif self.current_chapter_index < len(self.chapters):
            return f"Chapter {self.current_chapter_index + 1}- {self.chapters[self.current_chapter_index].get_chapter_name()}"
        
        return ''

    def get_objective_name(self) -> str:
        if self.current_chapter_index < len(self.chapters):
            return f"Objective- {self.chapters[self.current_chapter_index].get_objective()}"
        
        return 'Game Over'

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
                current_chapter.completion_action() # clear display between chapters?
                self.current_chapter_index += 1
