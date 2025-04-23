# Asteroids Roguelike Technical Context

## Technologies Used

The project is using the following technologies:

### Core Technologies

- **Python**: Primary programming language
- **Pygame**: Game development library for Python, handling rendering, input, and basic game mechanics

### Supporting Technologies

- **Git/GitHub**: Version control system
- **Pip**: Package management for Python dependencies

## Development Setup

### Environment Requirements

- Python 3.x installation
- Pygame library installed via pip
- Code editor/IDE with Python support

### Project Structure

The current project structure follows:

```mermaid
asteroids/
├── assets/ (Game assets)
├── src/ (Source code)
│   ├── __init__.py
│   ├── main.py (Game loop and primary controller)
│   ├── constants.py (Game constants and settings)
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── player.py (Player ship implementation)
│   │   ├── asteroid.py (Base asteroid implementation)
│   │   ├── elite_asteroid.py (Elite asteroid variants)
│   │   └── shot.py (Projectile implementation)
│   ├── managers/
│   │   ├── __init__.py
│   │   ├── asteroid_field.py (Asteroid spawning)
│   │   └── perk_manager.py (Perk generation and management)
│   ├── ui/
│   │   ├── __init__.py
│   │   └── ui_manager.py (UI screens and transitions)
│   └── utils/ (Utility functions)
├── venv/ (Python virtual environment)
└── memory-bank/ (Documentation)
```

## Technical Constraints

### Performance Considerations

- **Frame Rate**: Target 60 FPS for smooth gameplay
- **Entity Count**: Managed through controlled spawning of asteroids
- **Collision Detection**: Uses Pygame's sprite collision detection, optimized for circle-based entities

### Cross-Platform Compatibility

- Pygame runs on Windows, macOS, and Linux
- Game constants defined in constants.py for easy configuration

### Input Handling

- Keyboard controls for player movement and actions
- State-based UI for interacting with perk selection

## Dependencies

### Required Libraries

- **Pygame**: Primary game development framework
  - Handles rendering through Surface and Sprite classes
  - Provides input handling through pygame.event
  - Manages collision detection through sprite.spritecollide
  - Controls game timing through pygame.time.Clock

### Other Dependencies

- **Random**: Used for randomization of asteroid spawning, perk selection, and elite types
- **Sys**: For system-level operations like exiting the application

## Implementation Details

### Game Constants

Game parameters are defined in constants.py:

- Screen dimensions (1280x720)
- Asteroid properties (sizes, types)
- Player attributes (speed, health)
- Elite enemy settings (spawn chance, types)
- Game state constants

### Entity Management

Entities are managed through Pygame's sprite groups:

- updateables: All objects requiring per-frame updates
- drawables: All objects requiring rendering
- asteroids: Asteroid entities for collision detection
- shots: Projectile entities for collision detection

### State Management

Game flow is controlled through state constants:

- STATE_PLAYING: Active gameplay
- STATE_WAVE_TRANSITION: Between waves
- STATE_PERK_SELECTION: Perk selection UI
- STATE_GAME_OVER: Terminal state

## Technical Debt Considerations

Current technical debt areas:

- **UI Refinement**: The UI system works but could benefit from more abstraction for complex menus
- **Perk System Extension**: The foundation exists but needs expansion for more perk types
- **Performance Optimization**: May need refinement as entity count increases
- **Active Perk Implementation**: Framework exists but active perk mechanics need expansion
- **Visual Polish**: Basic rendering works but could benefit from additional visual effects

## Build and Distribution

The game is currently in active development with no packaging for distribution yet. Future distribution options could include:

- GitHub repository with source code
- Potentially packaged as executable using PyInstaller or cx_Freeze
