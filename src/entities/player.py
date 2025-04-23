import pygame

from src.utils.circleshape import CircleShape
from src.constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_MAX_HP,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from src.entities.shot import Shot


class Player(CircleShape):
    def __init__(self, x, y, shots_group):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shots = shots_group
        self.timer = 0
        # health points
        self.max_hp = PLAYER_MAX_HP
        self.hp = PLAYER_MAX_HP

        # Perk-related attributes
        self.perks = []
        self.speed_multiplier = 1.0
        self.fire_rate_multiplier = 1.0
        self.bullet_pierce = 0
        self.active_abilities = []

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # Draw the player ship
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

        # Draw active ability indicators if any
        ability_radius = self.radius + 5
        for i, ability in enumerate(self.active_abilities):
            angle_offset = i * 45  # Spread indicators around the ship
            indicator_pos = self.position + pygame.Vector2(0, ability_radius).rotate(self.rotation + angle_offset)
            pygame.draw.circle(screen, (0, 255, 0), indicator_pos, 3)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Ability keys (1-5)
        for i, key in enumerate([pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]):
            if keys[key] and i < len(self.active_abilities):
                self.use_ability(i)

        # Cooldown timer
        if self.timer > 0:
            self.timer -= dt * (1 + self.fire_rate_multiplier)

        # wrap around screen edges
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt * self.speed_multiplier

    def shoot(self):
        if self.timer > 0:
            # Don't print anything when on cooldown
            return
        else:
            new_shot = Shot(self.position.x, self.position.y)
            new_shot.velocity = (
                pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            )

            # Apply bullet pierce from perks
            if self.bullet_pierce > 0:
                new_shot.pierce = self.bullet_pierce

            self.shots.add(new_shot)
            self.timer = PLAYER_SHOOT_COOLDOWN / (1 + self.fire_rate_multiplier)

    def add_perk(self, perk):
        """Add a perk to the player and apply its effects"""
        self.perks.append(perk)
        perk.apply(self)

        # If it's an active ability, add it to the list
        if perk.effect_type == 'active':
            self.active_abilities.append(perk)

    def use_ability(self, index):
        """Use an active ability at the given index"""
        if index < len(self.active_abilities):
            ability = self.active_abilities[index]
            if not ability.active and ability.cooldown <= 0:
                # Implement ability effects here
                ability.active = True
                # Set cooldown
                ability.cooldown = ability.max_cooldown
                print(f"Used ability: {ability.name}")