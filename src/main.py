import sys
import random

import pygame

from src.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASTEROID_KINDS,
    ASTEROID_MIN_RADIUS,
    ELITE_MIN_WAVE,
    ELITE_SPAWN_CHANCE,
    ELITE_TYPES,
    WAVE_COUNTDOWN,
    PERK_SELECTION_AFTER_WAVE,
    STATE_PLAYING,
    STATE_WAVE_TRANSITION,
    STATE_PERK_SELECTION,
    STATE_GAME_OVER,
    PLAYER_SPEED,
    PLAYER_SHOOT_COOLDOWN
)
from src.entities.asteroid import Asteroid
from src.entities.elite_asteroid import create_elite_asteroid, EliteAsteroid, ExploderAsteroid, ShieldedAsteroid, SwarmLeaderAsteroid
from src.managers.asteroid_field import AsteroidField
from src.entities.player import Player
from src.entities.shot import Shot
from src.managers.perk_manager import PerkManager
from src.ui.ui_manager import UIManager

updateables = pygame.sprite.Group()
drawables = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()

Player.containers = (updateables, drawables)
Asteroid.containers = (asteroids, updateables, drawables)
EliteAsteroid.containers = (asteroids, updateables, drawables)
ExploderAsteroid.containers = (asteroids, updateables, drawables)
ShieldedAsteroid.containers = (asteroids, updateables, drawables)
SwarmLeaderAsteroid.containers = (asteroids, updateables, drawables)
AsteroidField.containers = updateables
Shot.containers = (shots, updateables, drawables)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Beaker's Revenge")
    clock = pygame.time.Clock()
    dt = 0

    # setup HUD: credits, wave number
    font = pygame.font.Font(None, 36)
    credits = 0
    wave = 1

    # Game state
    game_state = STATE_PLAYING

    # UI manager
    ui_manager = UIManager(screen)

    # Perk manager
    perk_manager = PerkManager()
    perks_available = []

    # Create player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shots)

    # helper to spawn waves of asteroids
    def spawn_wave(w):
        spawn_count = w * ASTEROID_KINDS

        for _ in range(spawn_count):
            edge = random.choice(AsteroidField.edges)
            # increase speed with wave
            speed = random.randint(40, 100) + (w - 1) * 10
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)

            # Check if we should spawn an elite asteroid
            is_elite = (w >= ELITE_MIN_WAVE and
                        random.random() < ELITE_SPAWN_CHANCE)

            if is_elite:
                elite_type = random.choice(ELITE_TYPES)
                # Use the factory function instead of direct instantiation
                asteroid = create_elite_asteroid(position.x, position.y,
                                        ASTEROID_MIN_RADIUS * kind,
                                        elite_type)
            else:
                asteroid = Asteroid(position.x, position.y, ASTEROID_MIN_RADIUS * kind)

            asteroid.velocity = velocity

    # Start the first wave with interlude
    ui_manager.show_wave_transition(wave, WAVE_COUNTDOWN)
    game_state = STATE_WAVE_TRANSITION

    # Function to handle perk selection
    def select_perk(perk):
        player.add_perk(perk)
        print(f"Selected perk: {perk.name}")

        # Show wave transition
        ui_manager.show_wave_transition(wave, WAVE_COUNTDOWN)
        return STATE_WAVE_TRANSITION

    # Main game loop
    running = True
    while running:
        # Process events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            # Add mouse click shooting when in playing state
            elif game_state == STATE_PLAYING and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.shoot()

        # Get UI updates
        ui_update = ui_manager.update(dt, events)

        # Process game state
        if game_state == STATE_WAVE_TRANSITION and ui_update:
            # Wave countdown finished, start the wave
            spawn_wave(wave)
            game_state = STATE_PLAYING

        elif game_state == STATE_PERK_SELECTION and ui_update:
            # Perk was selected, transition to next wave
            game_state = STATE_WAVE_TRANSITION

        # Check for held mouse button for continuous shooting
        if game_state == STATE_PLAYING:
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:  # Left mouse button held down
                player.shoot()

        # Clear the screen
        screen.fill("black")

        # Update game objects if in playing state
        if game_state == STATE_PLAYING:
            updateables.update(dt)

            # Check for collisions
            for asteroid in asteroids:
                # Check player collision
                if player.collision_check(asteroid):
                    # asteroid hits player
                    asteroid.kill()
                    player.hp -= 1
                    if player.hp <= 0:
                        print("Game over! Final credits:", credits)
                        game_state = STATE_GAME_OVER

                # Check shot collisions
                for shot in shots:
                    collision, attack_angle = shot.collision_check(asteroid)
                    if collision:
                        # Check if asteroid takes damage and is destroyed
                        if isinstance(asteroid, EliteAsteroid):
                            # Pass attack angle for shielded asteroids
                            is_destroyed = asteroid.take_damage(attack_angle)
                        else:
                            # Regular asteroids don't need attack angle
                            is_destroyed = asteroid.take_damage()

                        if is_destroyed:
                            # Add credits based on asteroid type
                            credits += asteroid.credits_value

                            # Handle asteroid splitting
                            if isinstance(asteroid, EliteAsteroid):
                                # Elite asteroids may have special splitting behavior
                                children = asteroid.split()
                                for child in children:
                                    asteroids.add(child)
                            else:
                                # Regular asteroids
                                children = asteroid.split()
                                for child in children:
                                    asteroids.add(child)

            # Check if wave is complete
            if not asteroids:
                wave += 1
                # Go to perk selection if enabled
                if PERK_SELECTION_AFTER_WAVE:
                    # Get random perks
                    perks_available = perk_manager.get_random_perks(3)
                    # Show perk selection screen
                    ui_manager.show_perk_selection(perks_available, select_perk)
                    game_state = STATE_PERK_SELECTION
                else:
                    # Go directly to next wave
                    ui_manager.show_wave_transition(wave, WAVE_COUNTDOWN)
                    game_state = STATE_WAVE_TRANSITION

        # Draw game objects
        for drawable in drawables:
            drawable.draw(screen)

        # Draw HUD information
        if game_state == STATE_PLAYING or game_state == STATE_WAVE_TRANSITION:
            # Game stats (credits, wave)
            cred_surf = font.render(f"Credits: {credits}", True, pygame.Color('white'))
            screen.blit(cred_surf, (10, 10))

            wave_surf = font.render(f"Wave: {wave}", True, pygame.Color('white'))
            screen.blit(wave_surf, (SCREEN_WIDTH - wave_surf.get_width() - 10, 10))

            # Player stats - vertical layout in top left
            y_offset = 50
            line_height = 30

            # HP display
            hp_base_text = f"HP: {player.hp}/{player.max_hp}"
            hp_surf = font.render(hp_base_text, True, pygame.Color('white'))
            screen.blit(hp_surf, (10, y_offset))
            y_offset += line_height

            # Speed display - base value + modifier
            speed_base = PLAYER_SPEED
            speed_mod = int(speed_base * player.speed_multiplier) - speed_base
            speed_base_text = f"Speed: {speed_base}"
            speed_surf = font.render(speed_base_text, True, pygame.Color('white'))
            screen.blit(speed_surf, (10, y_offset))

            # Add modifier in green if it exists
            if speed_mod != 0:
                mod_text = f"+{speed_mod}" if speed_mod > 0 else f"{speed_mod}"
                mod_surf = pygame.font.Font(None, 24).render(mod_text, True, pygame.Color('lime'))
                screen.blit(mod_surf, (10 + speed_surf.get_width() + 5, y_offset + 5))
            y_offset += line_height

            # Fire rate display - base value + modifier
            fire_rate_base = 1 / PLAYER_SHOOT_COOLDOWN
            fire_rate_mod = fire_rate_base * player.fire_rate_multiplier - fire_rate_base
            fire_rate_base_text = f"Fire Rate: {fire_rate_base:.1f}/s"
            fire_rate_surf = font.render(fire_rate_base_text, True, pygame.Color('white'))
            screen.blit(fire_rate_surf, (10, y_offset))

            # Add modifier in green if it exists
            if fire_rate_mod != 0:
                mod_text = f"+{fire_rate_mod:.1f}" if fire_rate_mod > 0 else f"{fire_rate_mod:.1f}"
                mod_surf = pygame.font.Font(None, 24).render(mod_text, True, pygame.Color('lime'))
                screen.blit(mod_surf, (10 + fire_rate_surf.get_width() + 5, y_offset + 5))
            y_offset += line_height

            # Bullet pierce display
            if player.bullet_pierce > 0:
                pierce_text = f"Pierce: {player.bullet_pierce}"
                pierce_surf = font.render(pierce_text, True, pygame.Color('white'))
                screen.blit(pierce_surf, (10, y_offset))
                y_offset += line_height

            # Active perks list
            if player.perks:
                perks_text = "Active Perks:"
                perks_surf = pygame.font.Font(None, 28).render(perks_text, True, pygame.Color('white'))
                screen.blit(perks_surf, (10, y_offset))
                y_offset += 25

                # List each perk on its own line
                perk_font = pygame.font.Font(None, 24)
                for perk in player.perks:
                    perk_surf = perk_font.render(f"• {perk.name}", True, pygame.Color('lime'))
                    screen.blit(perk_surf, (20, y_offset))
                    y_offset += 20

        # Draw game over screen
        if game_state == STATE_GAME_OVER:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            # Draw game over text
            game_over_font = pygame.font.Font(None, 72)
            game_over_surf = game_over_font.render("GAME OVER", True, pygame.Color('red'))
            screen.blit(game_over_surf, game_over_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))

            # Draw final score
            score_surf = font.render(f"Final Score: {credits}", True, pygame.Color('white'))
            screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))

            # Draw restart prompt
            restart_surf = font.render("Press R to restart or Q to quit", True, pygame.Color('white'))
            screen.blit(restart_surf, restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)))

            # Check for restart or quit
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Reset the game
                return main()  # Restart the game
            elif keys[pygame.K_q]:
                running = False

        # Draw UI elements
        ui_manager.draw()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        dt = clock.tick(60) / 1000

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()