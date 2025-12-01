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

## 🏗 Architecture Update (v2)
Refactoring has moved the engine towards a scalable, content-agnostic design:

*   **Unified `EntityManager`**: Replaced specific managers (`NPCManager`, `SourceManager`, etc.) with a single, generic system. New entities can be added without touching core engine code.
*   **Decoupled Dependencies**: Entities no longer require complex dependency injection; they query the `GameContext` dynamically to find targets (e.g., `context.get_entities(Source)`).
*   **Generic Game Loop**: The engine updates and renders all entities generically, regardless of their type.

## 🚀 Getting Started

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
