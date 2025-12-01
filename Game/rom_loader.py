"""
ROM Loader - Discovers and loads game ROMs (Story files)
"""
import os
import json
import importlib.util
import inspect
from typing import List, Dict, Optional, Type
from Game.story import Story


class ROMMetadata:
    """Holds metadata about a ROM"""
    def __init__(self, rom_dir: str, metadata: dict):
        self.rom_dir = rom_dir
        self.name = metadata.get("name", "Unknown ROM")
        self.version = metadata.get("version", "1.0.0")
        self.author = metadata.get("author", "Unknown")
        self.description = metadata.get("description", "No description available")
        self.main_file = metadata.get("main", "story.py")
        self.difficulty = metadata.get("difficulty", "Normal")
        self.tags = metadata.get("tags", [])
        
    def get_full_path(self) -> str:
        """Returns the full path to the main story file"""
        return os.path.join(self.rom_dir, self.main_file)


class ROMLoader:
    """Discovers and loads ROM files from the ROMs directory"""
    
    def __init__(self, roms_directory: str = "ROMs"):
        self.roms_directory = roms_directory
        self.available_roms: List[ROMMetadata] = []
        
    def scan_roms(self) -> List[ROMMetadata]:
        """Scans the ROMs directory and returns available ROMs"""
        self.available_roms = []
        
        if not os.path.exists(self.roms_directory):
            print(f"ROMs directory not found: {self.roms_directory}")
            return self.available_roms
            
        # Scan each subdirectory in the ROMs folder
        for item in os.listdir(self.roms_directory):
            rom_path = os.path.join(self.roms_directory, item)
            
            # Skip non-directories and __pycache__
            if not os.path.isdir(rom_path) or item == "__pycache__":
                continue
                
            # Look for rom.json metadata file
            metadata_path = os.path.join(rom_path, "rom.json")
            
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        rom_meta = ROMMetadata(rom_path, metadata)
                        self.available_roms.append(rom_meta)
                except Exception as e:
                    print(f"Error loading ROM metadata from {metadata_path}: {e}")
            else:
                # If no metadata file, create a basic one
                rom_meta = ROMMetadata(rom_path, {
                    "name": item,
                    "description": f"ROM: {item}"
                })
                self.available_roms.append(rom_meta)
                
        return self.available_roms
    
    def load_story_class(self, rom_metadata: ROMMetadata) -> Optional[Type[Story]]:
        """Loads the Story class from a ROM"""
        story_path = rom_metadata.get_full_path()
        
        if not os.path.exists(story_path):
            print(f"Story file not found: {story_path}")
            return None
            
        try:
            # Create a unique module name for this ROM
            module_name = f"rom_{rom_metadata.name.replace(' ', '_').lower()}"
            
            # Load module
            spec = importlib.util.spec_from_file_location(module_name, story_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find Story subclass
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Story) and obj is not Story:
                        return obj
                        
            print(f"No Story subclass found in {story_path}")
            return None
            
        except Exception as e:
            print(f"Error loading ROM: {e}")
            import traceback
            traceback.print_exc()
            return None

