# src/scenes/game_scene.py
import pygame
from settings import LOGICAL_WIDTH, LOGICAL_HEIGHT, PLAYER_SPEED
from src.utils.level_loader import load_level
from src.utils.camera import Camera               # ← новый импорт
from src.entities.player import Player
from src.entities.block import Block

class GameScene:
    def __init__(self, game):
        self.game = game
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.level_width, self.level_height = load_level(
            'level_01.tmx',
            self.player,
            self.blocks,
            self.all_sprites
        )

        if self.level_width == 0:
            print("⚠️ Создаю тестовый уровень")
            self._create_test_level()
            if not self.player.sprite:
                self.player.add(Player(100, LOGICAL_HEIGHT - 150))
            self.level_width = LOGICAL_WIDTH
            self.level_height = LOGICAL_HEIGHT
        else:
            print(f"✅ Уровень загружен, размер: {self.level_width}x{self.level_height}")

        # Создаём камеру с размерами экрана и карты
        self.camera = Camera(LOGICAL_WIDTH, LOGICAL_HEIGHT,
                             self.level_width, self.level_height)

    def _create_test_level(self):
        for i in range(0, LOGICAL_WIDTH, 50):
            block = Block(i, LOGICAL_HEIGHT - 50, 50, 50)
            self.blocks.add(block)
            self.all_sprites.add(block)
        platform = Block(300, 400, 100, 20)
        self.blocks.add(platform)
        self.all_sprites.add(platform)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.player.sprite:
                self.player.sprite.jump()

    def update(self):
        keys = pygame.key.get_pressed()
        if self.player.sprite:
            self.player.sprite.vel_x = 0
            if keys[pygame.K_LEFT]:
                self.player.sprite.vel_x = -PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                self.player.sprite.vel_x = PLAYER_SPEED

            self.player.sprite.update(self.blocks)
            # Обновляем камеру вслед за игроком
            self.camera.update(self.player.sprite)

    def draw(self, screen):
        # Отрисовываем все спрайты, применяя смещение камеры
        for sprite in self.all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))