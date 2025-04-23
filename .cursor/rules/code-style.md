# 🧼 Asteroids Roguelike Code Style

- Follow PEP 8 style guidelines for Python code
- Use clear, descriptive variable and function names
- Implement proper docstrings for all classes and functions
- Maintain consistent indentation (4 spaces)

## Docstrings

All classes and functions should have Google-style docstrings:

```python
def apply_perk(player, perk_type, value):
    """Apply a perk effect to the player.

    Args:
        player: The Player object to apply the perk to
        perk_type: String identifier of the perk type
        value: Numeric value or parameter for the perk

    Returns:
        bool: True if perk was successfully applied, False otherwise
    """
    # Function implementation
```

## Class Structure

Classes should follow this organization:

1. Class docstring
2. Class variables
3. `__init__` method
4. Properties
5. Public methods
6. Private methods (prefixed with `_`)

Example:

```python
class Asteroid:
    """Represents an asteroid entity in the game.

    Handles movement, collision, and special behaviors for asteroid objects.
    """

    # Class variables
    SIZE_LARGE = 3
    SIZE_MEDIUM = 2
    SIZE_SMALL = 1

    def __init__(self, x, y, size, is_elite=False):
        """Initialize an asteroid.

        Args:
            x: X-coordinate starting position
            y: Y-coordinate starting position
            size: Size category (1-3)
            is_elite: Whether this is an elite asteroid
        """
        self.x = x
        self.y = y
        self.size = size
        self.is_elite = is_elite
        self._setup_properties()

    @property
    def radius(self):
        """Calculate the collision radius based on size."""
        return self.size * 10

    def update(self, dt):
        """Update asteroid position based on velocity.

        Args:
            dt: Delta time since last update
        """
        # Method implementation

    def _setup_properties(self):
        """Initialize internal properties based on asteroid type."""
        # Private method implementation
```

## Comments

- Use comments to explain "why", not "what" (the code should be self-explanatory for "what")
- Add TODO comments for planned improvements: `# TODO: Implement difficulty scaling`
- Add comments for any complex algorithms or game mechanics
