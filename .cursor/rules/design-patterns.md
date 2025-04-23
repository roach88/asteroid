# 🧩 Asteroids Roguelike Design Patterns

## Implementation Patterns

- Use component-based design for game entities
- Implement state pattern for game flow management
- Follow factory pattern for creating game objects
- Utilize observer pattern for event handling

## Component-Based Design

Game entities should be composed of components that handle specific aspects of functionality:

```python
class Ship:
    def __init__(self, x, y):
        self.position = PositionComponent(x, y)
        self.physics = PhysicsComponent()
        self.health = HealthComponent(3)  # 3 initial health points
        self.renderer = ShipRendererComponent()
        self.weapon = WeaponComponent()

    def update(self, dt):
        self.physics.update(dt, self.position)
        self.weapon.update(dt)
        self.renderer.update(self.position)
```

## State Pattern

Game states should be implemented as discrete classes that manage different phases of gameplay:

```python
class GameState:
    def handle_input(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass

class GameplayState(GameState):
    def __init__(self, wave_number):
        self.wave_number = wave_number
        # Initialize gameplay elements

    # Override methods for gameplay state

class InterludeState(GameState):
    def __init__(self, available_perks, player_stats):
        self.available_perks = available_perks
        self.player_stats = player_stats
        # Initialize interlude UI

    # Override methods for interlude state
```

## Factory Pattern

Use factories to create game objects with varying properties:

```python
class AsteroidFactory:
    @staticmethod
    def create_asteroid(wave_number, position=None, size=None, is_elite=False):
        """Create an asteroid appropriate for the current wave.

        Args:
            wave_number: Current wave number for difficulty scaling
            position: Optional (x,y) tuple for position, or None for random
            size: Optional size override, or None for random
            is_elite: Whether to create an elite asteroid

        Returns:
            Asteroid: A configured asteroid instance
        """
        # Implementation to create appropriate asteroid
```

## Observer Pattern

Use an event system to decouple components:

```python
class EventManager:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self.listeners and listener in self.listeners[event_type]:
            self.listeners[event_type].remove(listener)

    def notify(self, event_type, data=None):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(data)

# Example usage
event_manager = EventManager()
event_manager.subscribe("asteroid_destroyed", score_manager.add_points)
event_manager.subscribe("wave_complete", ui_manager.show_interlude)
```

## Game-Specific Patterns

- Wave progression should scale difficulty using functions rather than simple multipliers
- Perks should be implemented as strategy objects that can be applied to the player
- Elite enemies should extend the base asteroid class with specialized behaviors
