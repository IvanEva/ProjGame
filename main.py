import pygame
import sys
from settings import *
from src.scenes.game_scene import GameScene

class Game:
    def __init__(self):
        pygame.init()
        self.PAUSE_KEY = PAUSE_KEY
        flags = 0
        if FULLSCREEN:
            flags |= pygame.FULLSCREEN
        if SCALED:
            flags |= pygame.SCALED

        self.screen = pygame.display.set_mode((LOGICAL_WIDTH, LOGICAL_HEIGHT), flags)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.game_scene = GameScene(self)
        self.current_scene = self.game_scene

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_scene.handle_event(event)

            self.current_scene.update()

            self.screen.fill(SKY_BLUE)
            self.current_scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()