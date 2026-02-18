import pygame
import sys
from settings import *
from src.scenes.game_scene import GameScene

class Game:
    def __init__(self):
        pygame.init()

        # Определяем флаги для режима отображения
        flags = 0
        if FULLSCREEN:
            flags |= pygame.FULLSCREEN
        if SCALED:
            flags |= pygame.SCALED

        self.screen = pygame.display.set_mode((LOGICAL_WIDTH, LOGICAL_HEIGHT), flags)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Загрузка фонового изображения (если есть)
        try:
            self.background = pygame.image.load(BACKGROUND_IMAGE).convert()
        except FileNotFoundError:
            print("Фоновое изображение не найдено, использую заливку цветом")
            self.background = None

        # Запускаем первую сцену (игровой уровень)
        self.current_scene = GameScene(self)

    def run(self):
        while self.running:
            # dt можно использовать для анимаций, но пока не нужно
            self.clock.tick(FPS)

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_scene.handle_event(event)

            # Обновление логики сцены
            self.current_scene.update()

            # Отрисовка фона
            if self.background:
                # Масштабируем фон под логическое разрешение
                bg_scaled = pygame.transform.scale(self.background,
                                                   (LOGICAL_WIDTH, LOGICAL_HEIGHT))
                self.screen.blit(bg_scaled, (0, 0))
            else:
                self.screen.fill(SKY_BLUE)

            # Отрисовка сцены поверх фона
            self.current_scene.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()