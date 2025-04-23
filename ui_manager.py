import pygame
import constants

class Button:
    def __init__(self, x, y, width, height, text, font, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False

    def draw(self, screen):
        # Draw button background
        color = (100, 100, 100) if self.hovered else (70, 70, 70)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        # Draw button text
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def update(self, mouse_pos, mouse_clicked):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_clicked and self.callback:
            self.callback()
            return True
        return False

class PerkCard:
    def __init__(self, x, y, width, height, perk, font, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.perk = perk
        self.font = font
        self.callback = callback
        self.hovered = False

    def draw(self, screen):
        # Draw card background
        color = (30, 100, 30) if self.hovered else (20, 70, 20)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        # Draw perk title
        title_font = pygame.font.Font(None, 28)
        title_surf = title_font.render(self.perk.name, True, (255, 255, 255))
        screen.blit(title_surf, (self.rect.x + 10, self.rect.y + 10))

        # Draw perk description
        desc_font = pygame.font.Font(None, 20)
        desc_surf = desc_font.render(self.perk.description, True, (200, 200, 200))
        screen.blit(desc_surf, (self.rect.x + 10, self.rect.y + 40))

    def update(self, mouse_pos, mouse_clicked):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_clicked and self.callback:
            self.callback(self.perk)
            return True
        return False

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.wave_transition = False
        self.perk_selection = False
        self.countdown = 0
        self.buttons = []
        self.perk_cards = []
        self.selected_perk = None

    def show_wave_transition(self, wave_num, countdown=3):
        self.wave_transition = True
        self.countdown = countdown
        self.wave_num = wave_num
        self.buttons = []

    def show_perk_selection(self, perks, callback):
        self.perk_selection = True
        self.perk_cards = []

        # Calculate positions for perk cards
        screen_center_x = constants.SCREEN_WIDTH // 2
        screen_center_y = constants.SCREEN_HEIGHT // 2
        card_width = 220
        card_height = 120
        card_spacing = 30

        start_x = screen_center_x - ((card_width * len(perks) + card_spacing * (len(perks) - 1)) // 2)

        for i, perk in enumerate(perks):
            x = start_x + i * (card_width + card_spacing)
            y = screen_center_y - (card_height // 2)
            self.perk_cards.append(PerkCard(x, y, card_width, card_height, perk, self.small_font, callback))

    def update(self, dt, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        if self.wave_transition:
            self.countdown -= dt
            if self.countdown <= 0:
                self.wave_transition = False
                return True  # Signal to start the wave

        if self.perk_selection:
            for card in self.perk_cards:
                if card.update(mouse_pos, mouse_clicked):
                    self.perk_selection = False
                    return True  # Signal that a perk was selected

        for button in self.buttons:
            if button.update(mouse_pos, mouse_clicked):
                return True

        return False

    def draw(self):
        if self.wave_transition:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            # Draw wave info
            wave_text = f"WAVE {self.wave_num}"
            wave_surf = self.font.render(wave_text, True, (255, 255, 255))
            text_rect = wave_surf.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(wave_surf, text_rect)

            # Draw countdown if > 0
            if self.countdown > 0:
                count_text = f"Starting in {int(self.countdown) + 1}..."
                count_surf = self.small_font.render(count_text, True, (255, 255, 255))
                count_rect = count_surf.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 + 20))
                self.screen.blit(count_surf, count_rect)

        if self.perk_selection:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            # Draw title
            title_text = "SELECT AN UPGRADE"
            title_surf = self.font.render(title_text, True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(title_surf, title_rect)

            # Draw perk cards
            for card in self.perk_cards:
                card.draw(self.screen)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)