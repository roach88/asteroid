import random
import pygame
import math

from src.entities.asteroid import Asteroid
from src.constants import ASTEROID_MIN_RADIUS

class EliteAsteroid(Asteroid):
    def __init__(self, x, y, radius, elite_type):
        super().__init__(x, y, radius)
        self.elite_type = elite_type
        self.color = self._get_elite_color()
        self.health = 2  # Elite asteroids take more hits
        self.credits_value = 3  # Elite asteroids give more credits

    def _get_elite_color(self):
        """Return the color based on elite type"""
        colors = {
            'exploder': (255, 100, 50),  # Red-orange
            'shielded': (50, 100, 255),  # Blue
            'swarm_leader': (200, 50, 200)  # Purple
        }
        return colors.get(self.elite_type, (255, 255, 255))

    def draw(self, screen):
        """Draw elite asteroid with color and effect"""
        pygame.draw.circle(screen, self.color, self.position, self.radius, 2)

        # Draw effect based on type
        if self.elite_type == 'exploder':
            # Draw small crosses inside
            size = self.radius * 0.3
            center = self.position
            pygame.draw.line(screen, self.color,
                            (center.x - size, center.y - size),
                            (center.x + size, center.y + size), 2)
            pygame.draw.line(screen, self.color,
                            (center.x - size, center.y + size),
                            (center.x + size, center.y - size), 2)

        elif self.elite_type == 'shielded':
            # Draw shield arc
            shield_rect = pygame.Rect(
                self.position.x - self.radius - 5,
                self.position.y - self.radius - 5,
                self.radius * 2 + 10,
                self.radius * 2 + 10
            )
            # Calculate angle based on velocity direction
            angle = pygame.Vector2(0, -1).angle_to(self.velocity)
            pygame.draw.arc(screen, self.color, shield_rect,
                          math.radians(angle - 45),
                          math.radians(angle + 45), 3)

        elif self.elite_type == 'swarm_leader':
            # Draw orbital circles
            pygame.draw.circle(screen, self.color, self.position, self.radius + 8, 1)
            pygame.draw.circle(screen, self.color, self.position, self.radius + 15, 1)

    def update(self, dt):
        """Update with elite behavior"""
        super().update(dt)

        # Extra behaviors based on type
        if self.elite_type == 'swarm_leader':
            # Swarm leaders could make nearby asteroids follow them
            # This would be implemented in main game loop to affect other asteroids
            pass

    def take_damage(self):
        """Elite asteroids can take multiple hits"""
        self.health -= 1
        return self.health <= 0

    def split(self):
        """Override split behavior depending on elite type"""
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return []

        # Different split behavior based on type
        children = []

        if self.elite_type == 'exploder':
            # Create more fragments
            for _ in range(5):  # More fragments
                angle = random.uniform(0, 360)
                new_vector = self.velocity.rotate(angle)
                new_radius = max(ASTEROID_MIN_RADIUS, self.radius / 3)

                new_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
                new_asteroid.velocity = new_vector * 1.5
                children.append(new_asteroid)

        elif self.elite_type in ['shielded', 'swarm_leader']:
            # Standard splitting but children maintain elite properties
            random_angle = random.uniform(20, 50)
            new_vector_1 = self.velocity.rotate(random_angle)
            new_vector_2 = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            if new_radius >= ASTEROID_MIN_RADIUS:
                new_asteroid_1 = EliteAsteroid(self.position.x, self.position.y, new_radius, self.elite_type)
                new_asteroid_2 = EliteAsteroid(self.position.x, self.position.y, new_radius, self.elite_type)
                new_asteroid_1.velocity = new_vector_1 * 1.2
                new_asteroid_2.velocity = new_vector_2
                children.append(new_asteroid_1)
                children.append(new_asteroid_2)

        return children