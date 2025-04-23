# 🐍 Asteroids Roguelike Python Guidelines

## Python Best Practices

- Use Python 3.x features fully
- Follow PEP 8 style guidelines
- Leverage pygame's built-in functionality effectively
- Apply object-oriented programming principles consistently

## Code Organization

- Keep files focused on a single responsibility
- Use classes to encapsulate related functionality
- Keep methods and functions reasonably sized (aim for <50 lines)
- Use modules to organize related classes

## Type Hints

Use type hints for better code clarity and IDE support:

```python
from typing import List, Tuple, Optional, Dict, Callable

def spawn_asteroids(
    count: int,
    positions: Optional[List[Tuple[float, float]]] = None
) -> List[Asteroid]:
    """Spawn a number of asteroids at specified positions or random locations.

    Args:
        count: Number of asteroids to spawn
        positions: Optional list of (x,y) coordinates, or None for random

    Returns:
        List of created Asteroid instances
    """
    # Implementation
```

## Pygame-Specific Patterns

### Surface Management

```python
# Create surfaces once and reuse them
self.ship_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.polygon(self.ship_surface, (255, 255, 255), [(0, 0), (32, 16), (0, 32)])

# In render method
screen.blit(self.ship_surface, (self.x, self.y))
```

### Time-Based Animation

All movement and animations should be time-based, not frame-based:

```python
def update(self, dt: float) -> None:
    """Update position based on velocity and time.

    Args:
        dt: Time elapsed since last update (in seconds)
    """
    self.x += self.velocity_x * dt
    self.y += self.velocity_y * dt
```

### Collision Detection

Use appropriate collision detection techniques:

```python
def check_collision(obj1, obj2):
    """Check if two objects are colliding using circle collision."""
    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y
    distance = (dx * dx + dy * dy) ** 0.5
    return distance < (obj1.radius + obj2.radius)
```

## Error Handling

- Use try/except blocks for operations that might fail
- Log errors for debugging
- Gracefully handle unexpected conditions:

```python
try:
    image = pygame.image.load(image_path)
except pygame.error as e:
    print(f"Error loading image: {e}")
    # Use fallback image or shape
    image = create_default_shape()
```

## Performance Tips

- Limit object creation during gameplay
- Use object pools for frequently created/destroyed objects
- Optimize collision detection with spatial partitioning for many objects
- Reduce unnecessary surface operations

## Testing

- Test critical game mechanics like collision detection
- Test perk effects to ensure they apply correctly
- Validate wave difficulty scaling functions
- Ensure game state transitions work as expected
