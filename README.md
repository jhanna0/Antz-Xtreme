# Antz Game Engine

## 🔮 The Vision
The goal of this project is to build a **generic, open-source game engine** for grid-based ASCII adventure games.

**The Core Engine** serves as a generic platform. It provides:
- Core Classes (Base Entity Types, basic functionality)
- Game Loop & Ticking System
- Rendering & Display
- Event System (Signals)
- Input Handling

**The ROMs** (Story files) act like game cartridges. They are responsible for:
- Defining specific Entities (e.g., "Zombie", "Potion", "Vending Machine")
- Registering these entities with the engine
- Defining Game Rules, Objectives, and Interactions

**The Goal:** The engine should be content-agnostic. It shouldn't know what a "Robot" is. Instead, it should read the ROM, which tells the engine: "Here is a Robot entity, here is how it looks, and here is how it acts." Everything—from characters to items—should be readable directly from the ROMs.

**Key Principle:** A creator should be able to define a new entity (e.g., a "Zombie" or "Trap") in their Story file *without* modifying the engine's core source code.

## 🚧 Current Status
The engine is currently a **functional prototype** running the "Antz Extreme" story. It features:
- ASCII Board Rendering.
- Turn-based movement.
- Basic Entity types: Players, NPCs (Robots), Sources (Resources), Machines, and Shops.
- A Chapter-based Story system.

## ⚠️ The Problems (Why Refactoring is Needed)
While the game works, the architecture is **brittle and tightly coupled**. It is currently very difficult for a user to extend the game without "hacking" the core.

### 1. "Manager Hell"
Currently, every entity type requires its own specific Manager class (e.g., `NPCManager`, `SourceManager`, `MachineManager`).
- **Problem:** If a user wants to add a `Zombie`, they must:
    1. Write a `Zombie` class.
    2. Write a `ZombieManager` class.
    3. Register the manager in `GameContext`.
    4. Ensure the Game Loop calls the new manager.
- **Goal:** Eliminate specific managers. The engine should have a generic way to handle *any* entity provided by the user.

### 2. Tight Coupling & Dependency Injection
Entities currently require their dependencies to be passed into their constructors.
- **Problem:** `NPC`s need references to `SourceManager` and `MachineManager` to function. This creates a web of dependencies that is hard to untangle.
- **Goal:** Entities should be able to query the "World" or "Context" dynamically to find what they need.

### 3. Hardcoded Game Loop
The `main.py` and `Game` class currently have hardcoded lists of what to update and render (e.g., `self.npcs`, `self.sources`).
- **Problem:** The engine "knows" too much about the specific content of the "Antz" game.
- **Goal:** The Game Loop should simply ask the generic storage to "update all entities," regardless of what they are.

---

## 🚀 Getting Started

WHENEVER YOU MODIFY THE DIR, COMPILE TO MAKE SURE IT WORKS:


### Prerequisites
- Python 3.7+

### Setup
1.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    ```
2.  **Activate the Virtual Environment:**
    *   MacOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   Windows:
        ```bash
        venv\Scripts\activate
        ```
3.  **Install Dependencies:**
    ```bash
    pip install pynput
    ```


### Running the Game
To play the included story:
```bash
python3 main.py
```
To run a custom story (if you have one):
```bash
python3 main.py --story path/to/your_story.py
```
