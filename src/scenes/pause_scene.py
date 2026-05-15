import pygame
import sys
from settings import LOGICAL_WIDTH, LOGICAL_HEIGHT

class PauseScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)

        self.options = ["Continue", "Quit"]
        self.selected = 0
        self.title_surf = self.font.render("PAUSED", True, (255, 255, 255))
        self.title_rect = self.title_surf.get_rect(center=(LOGICAL_WIDTH//2, LOGICAL_HEIGHT//3))
        self.option_rects = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.activate_selected()
            elif event.key == self.game.PAUSE_KEY:
                self.game.current_scene = self.game.game_scene

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected = i
                    self.activate_selected()

    def activate_selected(self):
        if self.options[self.selected] == "Continue":
            self.game.current_scene = self.game.game_scene
        elif self.options[self.selected] == "Quit":
            pygame.quit()
            sys.exit()

    def update(self):
        pass

    def draw(self, screen):
        overlay = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        screen.blit(self.title_surf, self.title_rect)

        self.option_rects = []
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text_surf = self.small_font.render(option, True, color)
            text_rect = text_surf.get_rect(center=(LOGICAL_WIDTH//2, LOGICAL_HEIGHT//2 + i * 60))
            screen.blit(text_surf, text_rect)
            self.option_rects.append(text_rect)