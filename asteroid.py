import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.health = 1  # Regular asteroids have 1 health
        self.credits_value = 1  # Credits given when destroyed

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        # move and wrap around the screen
        self.position += self.velocity * dt
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

    def take_damage(self):
        """Take damage and return True if destroyed"""
        self.health -= 1
        return self.health <= 0

    def split(self):
        """Split asteroid into smaller pieces"""
        self.kill()

        # Return list of child asteroids for simpler handling
        children = []

        if self.radius <= ASTEROID_MIN_RADIUS:
            return children
        else:
            random_angle = random.uniform(20, 50)
            new_vector_1 = self.velocity.rotate(random_angle)
            new_vector_2 = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS

            # Create new asteroids
            new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)

            # Set velocities
            new_asteroid_1.velocity = new_vector_1 * 1.2
            new_asteroid_2.velocity = new_vector_2

            # Add to children list
            children.append(new_asteroid_1)
            children.append(new_asteroid_2)

            return children
