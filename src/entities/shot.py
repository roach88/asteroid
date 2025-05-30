import pygame
import math

from src.utils.circleshape import CircleShape
from src.constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 0)
        self.pierce = 0  # How many additional enemies this shot can pierce
        self.lifetime = 2.0  # Shots disappear after 2 seconds

    def draw(self, screen):
        # Draw differently if it has pierce ability
        if self.pierce > 0:
            # Draw a filled circle with outline for piercing shots
            pygame.draw.circle(screen, "white", self.position, self.radius, 0)
            pygame.draw.circle(screen, (200, 200, 50), self.position, self.radius + 1, 1)
        else:
            # Standard shot
            pygame.draw.circle(screen, "white", self.position, self.radius, 0)

    def update(self, dt):
        # move and wrap around the screen
        self.position += self.velocity * dt

        # Check if shot is off-screen and remove if it is
        if (self.position.x < -self.radius or
            self.position.x > SCREEN_WIDTH + self.radius or
            self.position.y < -self.radius or
            self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()

        # Decrement lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def get_attack_angle(self, target_position):
        """
        Calculate the angle at which this shot is hitting the target
        Returns angle in degrees (0-360)
        """
        # Calculate direction vector from target to shot
        # This is the direction the shot is coming FROM relative to the target
        direction = self.position - target_position

        # Calculate angle in degrees (0-360) using atan2
        angle = math.degrees(math.atan2(direction.y, direction.x)) % 360

        return angle

    def collision_check(self, circle_object):
        """Check for collision and handle piercing"""
        if (self.position.distance_to(circle_object.position)
            < self.radius + circle_object.radius):

            # Calculate attack angle for the collision
            attack_angle = self.get_attack_angle(circle_object.position)

            if self.pierce > 0:
                # Reduce pierce count instead of destroying the shot
                self.pierce -= 1
                return True, attack_angle
            else:
                # Standard behavior - shot is destroyed on hit
                self.kill()
                return True, attack_angle

        return False, None