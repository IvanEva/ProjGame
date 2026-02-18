import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана (размеры окна)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Моя Terraria-подобная игра")

# Цвета (RGB)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# Частота кадров
clock = pygame.time.Clock()
FPS = 60

# Гравитация и скорость прыжка
GRAVITY = 0.5
JUMP_POWER = -12

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Пока просто прямоугольник, позже замените на спрайт
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

        # Проверка столкновений по горизонтали
        self.collide(self.vel_x, 0, blocks)

        # Вертикальное движение (гравитация)
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Проверка столкновений по вертикали
        self.on_ground = False
        self.collide(0, self.vel_y, blocks)

    def collide(self, dx, dy, blocks):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if dx > 0:  # Движение вправо
                    self.rect.right = block.rect.left
                if dx < 0:  # Движение влево
                    self.rect.left = block.rect.right
                if dy > 0:  # Падение вниз
                    self.rect.bottom = block.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                if dy < 0:  # Прыжок вверх (удар головой)
                    self.rect.top = block.rect.bottom
                    self.vel_y = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER

# Класс блока (земли/платформы)
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()

# Создание уровня из блоков (пример)
def create_level():
    # Земля
    for i in range(0, SCREEN_WIDTH, 50):
        block = Block(i, SCREEN_HEIGHT - 50, 50, 50)
        blocks.add(block)
        all_sprites.add(block)
    # Платформа
    platform = Block(300, 400, 100, 20)
    blocks.add(platform)
    all_sprites.add(platform)

create_level()

# Создание игрока
player = Player(100, SCREEN_HEIGHT - 150)
all_sprites.add(player)

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Получение нажатых клавиш
    keys = pygame.key.get_pressed()
    player.vel_x = 0
    if keys[pygame.K_LEFT]:
        player.vel_x = -5
    if keys[pygame.K_RIGHT]:
        player.vel_x = 5

    # Обновление игрока
    player.update(blocks)

    # Отрисовка
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()