# 📁 Asteroids Roguelike Project Structure

- Follow the established pygame project structure for code organization
- Keep assets separate from code in dedicated directories
- Use clear, descriptive naming for all classes and functions

## Directory Layout

```mermaid
asteroids/
├── assets/              # All game assets
│   ├── images/          # Sprite images and visual elements
│   ├── sounds/          # Sound effects and music
│   └── fonts/           # Text fonts
├── src/                 # Source code
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── game.py          # Main game controller
│   ├── entities/        # Game entities
│   │   ├── __init__.py
│   │   ├── player.py    # Player ship
│   │   ├── asteroid.py  # Asteroid objects
│   │   └── projectile.py # Bullets and other projectiles
│   ├── managers/        # Game systems
│   │   ├── __init__.py
│   │   ├── wave_manager.py  # Wave progression system
│   │   └── perk_manager.py  # Perk selection and application
│   └── ui/              # User interface elements
│       ├── __init__.py
│       ├── hud.py       # In-game HUD
│       └── interlude.py # Between-wave screens
└── memory-bank/         # Documentation
    ├── activeContext.md
    ├── productContext.md
    ├── progress.md
    ├── projectBrief.md
    ├── systemPatterns.md
    └── techContext.md
```

## Naming Conventions

- Class names: `CamelCase` (e.g., `WaveManager`, `EliteAsteroid`)
- Functions and methods: `snake_case` (e.g., `spawn_asteroids()`, `apply_perk()`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_PLAYER_HEALTH`, `BASE_ASTEROID_SPEED`)
- Modules: `snake_case` (e.g., `wave_manager.py`, `player.py`)

## Import Organization

- Group imports in this order:
  1. Standard library imports
  2. Third-party imports (pygame)
  3. Local application imports
- Use absolute imports for clarity
