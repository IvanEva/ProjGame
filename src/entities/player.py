import pygame
from settings import GRAVITY, PLAYER_JUMP_POWER, BLUE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self, blocks):
        # Горизонтальное движение
        self.rect.x += self.vel_x
        self.collide(self.vel_x, 0, blocks)

        # Вертикальное движение
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False
        self.collide(0, self.vel_y, blocks)

    def collide(self, dx, dy, blocks):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if dx > 0:
                    self.rect.right = block.rect.left
                elif dx < 0:
                    self.rect.left = block.rect.right
                if dy > 0:
                    self.rect.bottom = block.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif dy < 0:
                    self.rect.top = block.rect.bottom
                    self.vel_y = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = PLAYER_JUMP_POWER