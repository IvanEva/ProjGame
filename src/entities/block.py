import pygame
from settings import BROWN, GREEN   # GREEN добавьте в settings.py, если его нет

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, one_way=False):
        super().__init__()
        self.image = pygame.Surface((width, height))
        # Для наглядности односторонние платформы будут зелёными
        if one_way:
            self.image.fill(GREEN)
        else:
            self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.one_way = one_way   # сохраняем свойство для обработки коллизий