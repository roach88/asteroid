# Asteroids Roguelike System Patterns

## System Architecture

The Asteroids Roguelike game follows a component-based architecture typical of 2D arcade games, with the following high-level components:

1. **Game Loop**: Core pygame loop handling rendering, input, and time management
2. **Entity System**: Objects including player ship, asteroids, bullets, and visual effects
3. **Wave Manager**: Controls spawning patterns, wave progression, and difficulty scaling
4. **Perk System**: Manages available perks, selection UI, and applying effects to gameplay
5. **UI System**: Handles game state transitions, menus, and info displays

## Key Technical Decisions

### Pygame Framework

The project appears to use pygame for rendering and game management, which provides:

- Simple 2D rendering capabilities
- Input handling
- Basic collision detection
- Audio support

### State Management

Game progression will be managed through distinct states:

- Gameplay State (active wave)
- Interlude State (between waves, selection screen)
- Game Over State

### Entity Enhancement System

A flexible system for perks to modify player or bullet properties dynamically during gameplay.

## Design Patterns in Use

### Component Pattern

Entities will have components that define their behavior:

- **Rendering Component**: Visual representation
- **Physics Component**: Movement, rotation, collision
- **Behavior Component**: AI patterns for asteroids/enemies

### Factory Pattern

For generating:

- Asteroids with varying properties
- Elite enemies with specialized behaviors
- Perks with different effects

### Observer Pattern

For event handling:

- Wave completion events
- Player damage/death events
- Perk activation triggers

### Strategy Pattern

For behavior implementation:

- Different movement strategies for asteroids
- Various elite enemy behaviors
- Perk effect implementations

## Component Relationships

```mermaid
Game Controller
├── Wave Manager
│   ├── Asteroid Spawner
│   └── Difficulty Scaler
├── Player Controller
│   ├── Input Handler
│   ├── Ship Physics
│   └── Weapon System
├── Perk Manager
│   ├── Perk Factory
│   └── Effect Applicator
├── UI Controller
│   ├── HUD Elements
│   └── Wave Interlude UI
└── Collision System
```

## Data Flow

1. Game loop updates all entities
2. Player input affects ship movement and firing
3. Collision system detects interactions
4. Wave manager tracks asteroid destruction
5. When wave completes, interlude UI activates
6. Player selects perk, perk manager applies effects
7. New wave begins with adjusted difficulty
