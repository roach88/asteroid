# 🎮 Asteroids Roguelike Gameplay Patterns

## Project-Specific Patterns

- Always track wave number in the game state
- Store player perks in a persistent collection during gameplay session
- Scale enemy difficulty based on wave number
- Use interlude screens between gameplay waves
- Implement clear visual distinction for elite enemies

## Wave Management

- Track the current wave number in the game state
- Use a countdown timer (3 seconds) before starting each new wave
- Display wave number prominently at the start of each wave
- Scale wave difficulty using formulas based on wave number:

```python
def calculate_asteroid_count(wave_number):
    """Calculate the number of asteroids for the given wave."""
    # Base count + scaling formula
    return 5 + int(wave_number * 1.5)

def calculate_elite_chance(wave_number):
    """Calculate the probability of spawning an elite asteroid."""
    # No elites before wave 5, then increasing chance
    if wave_number < 5:
        return 0
    return min(0.4, 0.05 * (wave_number - 4))  # Cap at 40%
```

## Perk System

- Present exactly 3 random perks after each wave
- Store all acquired perks in a player's perk collection
- Apply cumulative effects of all perks to gameplay:

```python
class PerkManager:
    def __init__(self):
        self.active_perks = []

    def add_perk(self, perk):
        self.active_perks.append(perk)
        perk.apply_effect()

    def get_available_perks(self, count=3):
        """Get a random selection of perks for player to choose from."""
        # Implementation to select perks

    def apply_all_effects(self, player):
        """Apply all perk effects to the player."""
        for perk in self.active_perks:
            perk.apply_effect(player)
```

## Elite Enemies

- Elite enemies should appear starting at wave 5
- Each elite type should have a distinct visual indicator:

  - Exploder: Red pulsing outline
  - Shielded: Blue shield effect
  - Swarm Leader: Purple aura

- Implement specialized behaviors:

```python
class ExploderAsteroid(Asteroid):
    """Elite asteroid that explodes into fragments when destroyed."""

    def on_destroy(self):
        # Create multiple fragment asteroids
        for i in range(5):
            # Create and add smaller, faster asteroid fragment

class ShieldedAsteroid(Asteroid):
    """Elite asteroid that takes reduced damage from frontal attacks."""

    def take_damage(self, damage, hit_angle):
        # Reduce damage if hit from the front
        if self.is_frontal_hit(hit_angle):
            damage *= 0.25
        super().take_damage(damage)
```

## User Experience

- Support keyboard controls with WASD or arrow keys for movement
- Provide visual feedback for all player actions, including:

  - Flash effects for shooting
  - Screen shake for taking damage
  - Pulsing effects for perk acquisition

- Keep UI minimal during gameplay, showing only:

  - Current health
  - Wave number
  - Active perks (small icons)

- During interlude screens, display:
  - Wave completion stats
  - Clear perk choices with descriptions
  - Preview of next wave difficulty
