# ROMs Directory

This directory contains game ROMs (story files) for the Antz Game Engine.

## ROM Structure

Each ROM should be in its own subdirectory with the following structure:

```
ROMs/
├── YourROMName/
│   ├── __init__.py          # Package marker
│   ├── rom.json             # ROM metadata
│   ├── story.py             # Main story file (contains Story subclass)
│   └── pieces.py            # Custom entities/pieces (optional)
```

## ROM Metadata (rom.json)

Each ROM must include a `rom.json` file with the following structure:

```json
{
  "name": "Your ROM Name",
  "version": "1.0.0",
  "author": "Your Name",
  "description": "A brief description of your ROM/story",
  "main": "story.py",
  "difficulty": "Easy|Normal|Hard",
  "tags": ["tag1", "tag2", "tag3"]
}
```

### Fields:
- **name**: Display name for your ROM
- **version**: Semantic version number
- **author**: Creator's name
- **description**: Brief description shown in menu (keep it concise)
- **main**: Python file containing the Story class (usually "story.py")
- **difficulty**: Difficulty level (Easy, Normal, or Hard)
- **tags**: Array of tags to categorize your ROM

## Creating a New ROM

1. Create a new directory in `ROMs/` with your ROM name
2. Add `__init__.py` (can be empty or contain package info)
3. Create `rom.json` with your ROM's metadata
4. Create your main story file (e.g., `story.py`) with a `Story` subclass
5. Optionally create additional files for custom entities

## Story Class Requirements

Your main story file must contain a class that inherits from `Game.story.Story`:

```python
from Game.story import Story, Chapter
from Game.context import GameContext

class YourStory(Story):
    def __init__(self, context: GameContext, kb_func: callable):
        super().__init__(name="Your ROM Name")
        self.context = context
        # Initialize chapters, etc.
    
    def setup(self, game):
        # Setup game state, create player, etc.
        pass
    
    def start(self):
        # Called when the game starts
        super().start()
    
    def every_turn(self):
        # Called every game tick
        pass
```

## Example: Antz Extreme ROM

See the `AntzExtreme` directory for a complete example of a ROM implementation.

## Loading ROMs

ROMs are automatically discovered and displayed in the main menu when you run:

```bash
python3 main.py
```

You can also load a specific ROM directly:

```bash
python3 main.py --rom "ROM Name"
```

Or load a story file directly (bypassing the ROM system):

```bash
python3 main.py --story path/to/story.py
```

