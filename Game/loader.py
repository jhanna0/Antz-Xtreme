import importlib.util
import inspect
import os
from typing import Type, Optional
from Game.story import Story

def load_story_from_file(file_path: str) -> Optional[Type[Story]]:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    try:
        # Load module
        spec = importlib.util.spec_from_file_location("custom_story", file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find Story subclass
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Story) and obj is not Story:
                    print(f"Found story: {name}")
                    return obj
        print("No Story subclass found in file.")
        return None
    except Exception as e:
        print(f"Error loading story: {e}")
        return None

