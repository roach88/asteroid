# Asteroids Roguelike System Patterns

## System Architecture

The Asteroids Roguelike game follows a component-based architecture typical of 2D arcade games. The implementation has materialized with these components:

1. **Game Loop**: Core pygame loop in `main.py` handling rendering, input, and time management
2. **Entity System**: Objects including Player, Asteroids (regular and elite), and Shots
3. **Wave Manager**: Controls spawning patterns, wave progression, and difficulty scaling
4. **Perk System**: PerkManager class handling available perks, selection, and application
5. **UI System**: UIManager handling game state transitions, menus, and information displays

## Key Technical Decisions

### Pygame Framework

The project uses pygame for rendering and game management:

- 2D rendering for all game entities
- Input handling for player controls
- Sprite-based collision detection
- State management system for game flow

### State Management

Game progression is managed through distinct states implemented as constants:

- `STATE_PLAYING`: Active gameplay during a wave
- `STATE_WAVE_TRANSITION`: Between waves, showing countdown
- `STATE_PERK_SELECTION`: Player choosing perks after a wave
- `STATE_GAME_OVER`: Terminal state when player loses

### Entity Enhancement System

Perks modify player or bullet properties through:

- Player.add_perk() method applying perk effects
- PerkManager generating and tracking available perks
- Perk effects modifying player attributes or behaviors

## Design Patterns in Use

### Component Pattern

Entities have components that define their behavior:

- **Sprite-based Rendering**: All entities extend pygame.sprite.Sprite
- **Physics**: Velocity and position management in entity update methods
- **Behavior**: Specialized behaviors for different entity types

### Factory Pattern

Generation of game elements:

- AsteroidField handles asteroid spawning with edge selection
- PerkManager creates randomized perk selections
- Wave spawning creates the appropriate mix of regular and elite asteroids

### Observer Pattern

Event handling through:

- UI state transitions based on game events
- Wave completion detection triggering perk selection
- Collision detection initiating appropriate responses

### Strategy Pattern

Behavior implementation:

- Elite asteroid types with distinct behaviors (Exploder, Shielded, Swarm Leader)
- Different movement strategies for asteroids
- Perk effect implementations

## Component Relationships

The current implementation structure follows this organization:

```mermaid
main.py (Game Controller)
├── Game State Management
│   ├── STATE_PLAYING
│   ├── STATE_WAVE_TRANSITION
│   ├── STATE_PERK_SELECTION
│   └── STATE_GAME_OVER
├── entities/
│   ├── player.py (Player Controller)
│   │   ├── Movement & Physics
│   │   ├── Shooting Mechanism
│   │   └── Perk Application
│   ├── asteroid.py (Base Asteroid)
│   ├── elite_asteroid.py (Specialized Asteroids)
│   └── shot.py (Projectiles)
├── managers/
│   ├── asteroid_field.py (Spawn Control)
│   └── perk_manager.py (Perk Generation)
└── ui/
    └── ui_manager.py (Interface Control)
        ├── Wave Transition UI
        └── Perk Selection Interface
```

## Data Flow

1. Game loop updates all entities in updateables group
2. Player input affects ship movement and firing
3. Collision system detects interactions between shots, asteroids, and player
4. Wave completion is detected when asteroids group is empty
5. When wave completes, interlude UI activates followed by perk selection
6. Player selects perk, perk manager applies effects
7. New wave begins with adjusted difficulty based on wave number

## Entity Management

The game uses pygame sprite groups for efficient entity management:

- `updateables`: All objects needing per-frame updates
- `drawables`: All objects requiring rendering
- `asteroids`: All asteroid entities for collision detection
- `shots`: All projectiles for collision detection

Each entity type registers with the appropriate containers on instantiation, allowing for clean separation of concerns and efficient group operations.
