import pygame
from src.entities.player import Player
from src.entities.block import Block
from settings import LOGICAL_WIDTH, LOGICAL_HEIGHT, PLAYER_SPEED

class GameScene:
    def __init__(self, game):
        self.game = game
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        self.create_level()

        self.player = Player(100, LOGICAL_HEIGHT - 150)
        self.all_sprites.add(self.player)

    def create_level(self):
        # Земля внизу (блоки 50x50)
        for i in range(0, LOGICAL_WIDTH, 50):
            block = Block(i, LOGICAL_HEIGHT - 50, 50, 50)
            self.blocks.add(block)
            self.all_sprites.add(block)
        # Одиночная платформа
        platform = Block(300, 400, 100, 20)
        self.blocks.add(platform)
        self.all_sprites.add(platform)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.jump()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.player.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.player.vel_x = PLAYER_SPEED

        self.player.update(self.blocks)

    def draw(self, screen):
        self.all_sprites.draw(screen)