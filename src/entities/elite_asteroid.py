import random
import pygame
import math

from src.entities.asteroid import Asteroid
from src.constants import ASTEROID_MIN_RADIUS

class EliteAsteroid(Asteroid):
    """Base class for all Elite Asteroids with common functionality"""

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Common properties all elites share
        self.health = 3
        self.credits_value = 5
        self.time_alive = 0

    def update(self, dt):
        """Update with base elite behavior"""
        super().update(dt)
        self.time_alive += dt

        # Subclasses will implement specific behaviors
        self.special_behavior(dt)

    def special_behavior(self, dt):
        """To be implemented by subclasses"""
        pass

    def take_damage(self, attack_angle=None):
        """Base damage handling for elites"""
        self.health -= 1
        return self.health <= 0

    def create_standard_children(self):
        """Create standard asteroid children"""
        random_angle = random.uniform(20, 50)
        new_vector_1 = self.velocity.rotate(random_angle)
        new_vector_2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        children = []

        if new_radius >= ASTEROID_MIN_RADIUS:
            # Create child asteroids of the same class
            child_class = self.__class__
            new_asteroid_1 = child_class(self.position.x, self.position.y, new_radius)
            new_asteroid_2 = child_class(self.position.x, self.position.y, new_radius)

            # Reduce health for children
            new_asteroid_1.health = max(2, self.health - 1)
            new_asteroid_2.health = max(2, self.health - 1)

            new_asteroid_1.velocity = new_vector_1 * 1.2
            new_asteroid_2.velocity = new_vector_2

            children.append(new_asteroid_1)
            children.append(new_asteroid_2)

        return children


class ExploderAsteroid(EliteAsteroid):
    """Elite asteroid that explodes into multiple fragments when destroyed"""

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.explosion_primed = False
        self.color = (255, 100, 50)  # Red-orange

    def draw(self, screen):
        """Draw exploder asteroid with crosses inside"""
        # Draw base asteroid with pulsing effect - higher frequency and wider amplitude
        intensity = (math.sin(self.time_alive * 8) * 0.5) + 0.7
        pulse_color = tuple(min(255, int(c * intensity)) for c in self.color)

        # Draw the asteroid base
        pygame.draw.circle(screen, pulse_color, self.position, self.radius, 2)

        # Draw crosses inside
        size = self.radius * 0.3
        center = self.position

        # Make the cross pulse if primed to explode
        line_width = 3 if self.explosion_primed else 2

        # Additional pulsing effect for the cross size when primed
        if self.explosion_primed:
            pulse_size = size * (0.8 + math.sin(self.time_alive * 10) * 0.2)
        else:
            pulse_size = size

        pygame.draw.line(screen, pulse_color,
                        (center.x - pulse_size, center.y - pulse_size),
                        (center.x + pulse_size, center.y + pulse_size), line_width)
        pygame.draw.line(screen, pulse_color,
                        (center.x - pulse_size, center.y + pulse_size),
                        (center.x + pulse_size, center.y - pulse_size), line_width)

    def special_behavior(self, dt):
        """Randomly prime for explosion when health is low"""
        if self.health <= 2 and not self.explosion_primed and random.random() < 0.005:
            self.explosion_primed = True

    def take_damage(self, attack_angle=None):
        """Take damage and potentially prime for explosion"""
        self.health -= 1

        # Chance to prime explosion when damaged
        if not self.explosion_primed and self.health <= 2 and random.random() < 0.3:
            self.explosion_primed = True

        return self.health <= 0

    def split(self):
        """Split into more fragments when destroyed"""
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return []

        # Create more fragments
        children = []
        fragment_count = 8 if self.explosion_primed else 5  # More fragments if primed

        for _ in range(fragment_count):
            angle = random.uniform(0, 360)
            new_vector = self.velocity.rotate(angle)
            new_radius = max(ASTEROID_MIN_RADIUS, self.radius / 3)

            new_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid.velocity = new_vector * (2.0 if self.explosion_primed else 1.5)
            children.append(new_asteroid)

        return children


class ShieldedAsteroid(EliteAsteroid):
    """Elite asteroid with a shield that reduces damage from certain angles"""

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.health = 4  # Shielded asteroids are tougher
        self.damage_reduction = 0.5
        self.shield_active = True
        self.shield_angle = 0
        self.shield_arc_width = 180  # Degrees - wider arc
        self.color = (50, 100, 255)  # Blue
        self.rotation_speed = 45  # Degrees per second

    def draw(self, screen):
        """Draw shielded asteroid with shield arc"""
        # Draw base asteroid with pulsing effect
        intensity = (math.sin(self.time_alive * 5) * 0.3) + 0.7
        pulse_color = tuple(min(255, int(c * intensity)) for c in self.color)

        # Draw the asteroid base
        pygame.draw.circle(screen, pulse_color, self.position, self.radius, 2)

        # Draw shield arc
        if self.shield_active:
            shield_rect = pygame.Rect(
                self.position.x - self.radius - 5,
                self.position.y - self.radius - 5,
                self.radius * 2 + 10,
                self.radius * 2 + 10
            )

            half_width = self.shield_arc_width / 2

            # Draw shield with thickness based on damage reduction
            shield_thickness = 3 + int(self.damage_reduction * 3)
            pygame.draw.arc(screen, pulse_color, shield_rect,
                        math.radians(self.shield_angle - half_width),
                        math.radians(self.shield_angle + half_width), shield_thickness)

    def special_behavior(self, dt):
        """Rotate shield quickly around the asteroid"""
        # Faster rotation speed and continuous movement
        self.shield_angle = (self.shield_angle + self.rotation_speed * dt) % 360

    def is_vulnerable_to_attack(self, attack_angle):
        """Check if vulnerable from a specific angle"""
        half_width = self.shield_arc_width / 2

        # Check if attack angle is outside shield arc
        min_angle = (self.shield_angle - half_width) % 360
        max_angle = (self.shield_angle + half_width) % 360

        if min_angle < max_angle:
            return attack_angle < min_angle or attack_angle > max_angle
        else:
            # Handle wrap-around case
            return attack_angle < min_angle and attack_angle > max_angle

    def take_damage(self, attack_angle=None):
        """Take damage based on attack angle"""
        if attack_angle is not None:
            # Check if attack hits shield
            if not self.is_vulnerable_to_attack(attack_angle):
                # Hit shield - reduced damage
                self.health -= 0.5
            else:
                # Hit vulnerable spot - full damage
                self.health -= 1
        else:
            # No angle provided, use standard damage reduction
            self.health -= (1 - self.damage_reduction)

        return self.health <= 0

    def split(self):
        """Split into smaller shielded asteroids"""
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return []

        return self.create_standard_children()


class SwarmLeaderAsteroid(EliteAsteroid):
    """Elite asteroid that makes unpredictable movements and influences nearby asteroids"""

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.influence_radius = radius * 5
        self.color = (200, 50, 200)  # Purple

    def draw(self, screen):
        """Draw swarm leader with orbital rings"""
        # Draw base asteroid with pulsing effect
        intensity = (math.sin(self.time_alive * 5) * 0.3) + 0.7
        pulse_color = tuple(min(255, int(c * intensity)) for c in self.color)

        # Draw the asteroid base
        pygame.draw.circle(screen, pulse_color, self.position, self.radius, 2)

        # Draw orbital circles that pulse
        pulse_radius_1 = self.radius + 8 + (math.sin(self.time_alive * 3) * 3)
        pulse_radius_2 = self.radius + 15 + (math.sin(self.time_alive * 3 + 1) * 3)

        pygame.draw.circle(screen, pulse_color, self.position, pulse_radius_1, 1)
        pygame.draw.circle(screen, pulse_color, self.position, pulse_radius_2, 1)

    def special_behavior(self, dt):
        """Make unpredictable turns occasionally"""
        if random.random() < 0.01:
            # Make a sharper turn
            turn_angle = random.choice([-45, 45])
            self.velocity = self.velocity.rotate(turn_angle)

    def split(self):
        """Split into smaller swarm leaders"""
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return []

        return self.create_standard_children()


# Factory function to create the right type of elite asteroid
def create_elite_asteroid(x, y, radius, elite_type):
    """Factory function to create elite asteroids of the specified type"""
    elite_classes = {
        'exploder': ExploderAsteroid,
        'shielded': ShieldedAsteroid,
        'swarm_leader': SwarmLeaderAsteroid
    }

    elite_class = elite_classes.get(elite_type)
    if elite_class:
        return elite_class(x, y, radius)
    else:
        # Fallback to base class if type not found
        asteroid = EliteAsteroid(x, y, radius)
        asteroid.color = (255, 255, 255)  # White as fallback
        return asteroid