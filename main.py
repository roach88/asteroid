import sys

import pygame

import constants
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

    # Create player and asteroid field
    player = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, shots)
    # asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updateables.update(dt)
        for asteroid in asteroids:
            if player.collision_check(asteroid):
                print("Game over!")
                sys.exit()
            for shot in shots:
                if shot.collision_check(asteroid):
                    shot.kill()
                    asteroid.split()
        for drawable in drawables:
            drawable.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        player.timer -= dt


if __name__ == "__main__":
    main()
