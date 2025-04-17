import sys

import pygame

import constants
import random
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shot import Shot

updateables = pygame.sprite.Group()
drawables = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()

Player.containers = (updateables, drawables)
Asteroid.containers = (asteroids, updateables, drawables)
AsteroidField.containers = updateables
Shot.containers = (shots, updateables, drawables)


def main():
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    # setup HUD: credits, wave number
    font = pygame.font.Font(None, 36)
    credits = 0
    wave = 1

    # Create player
    player = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, shots)

    # helper to spawn waves of asteroids
    def spawn_wave(w):
        for _ in range(w * constants.ASTEROID_KINDS):
            edge = random.choice(AsteroidField.edges)
            # increase speed with wave
            speed = random.randint(40, 100) + (w - 1) * 10
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, constants.ASTEROID_KINDS)
            ast = Asteroid(position.x, position.y, constants.ASTEROID_MIN_RADIUS * kind)
            ast.velocity = velocity

    # start first wave
    spawn_wave(wave)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updateables.update(dt)
        # collision detection & run scoring
        for asteroid in asteroids:
            if player.collision_check(asteroid):
                # asteroid hits player
                asteroid.kill()
                player.hp -= 1
                if player.hp <= 0:
                    print("Game over! Final credits:", credits)
                    sys.exit()
            for shot in shots:
                if shot.collision_check(asteroid):
                    shot.kill()
                    asteroid.split()
                    credits += 1

        # on wave clear, spawn next
        if not asteroids:
            wave += 1
            spawn_wave(wave)
        for drawable in drawables:
            drawable.draw(screen)
        # draw HUD: credits, HP, wave
        cred_surf = font.render(f"Credits: {credits}", True, pygame.Color('white'))
        screen.blit(cred_surf, (10, 10))
        hp_surf = font.render(f"HP: {player.hp}/{player.max_hp}", True, pygame.Color('white'))
        screen.blit(hp_surf, (10, 50))
        wave_surf = font.render(f"Wave: {wave}", True, pygame.Color('white'))
        screen.blit(wave_surf, (constants.SCREEN_WIDTH - wave_surf.get_width() - 10, 10))
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        player.timer -= dt


if __name__ == "__main__":
    main()
