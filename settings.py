import os
import pygame   # <-- добавлен импорт pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
BACKGROUNDS_DIR = os.path.join(IMAGES_DIR, 'backgrounds')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
LEVELS_DIR = os.path.join(ASSETS_DIR, 'levels')
PLAYER_ANIMATIONS_DIR = os.path.join(IMAGES_DIR, 'characters', 'player')

# Разрешение (логическое)
LOGICAL_WIDTH = 1920
LOGICAL_HEIGHT = 1080

# Режим экрана
FULLSCREEN = True
SCALED = True
FPS = 30
TITLE = "Platformer Game"

# Цветы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)

# Физика
PLAYER_SPEED = 5          # обычная ходьба
PLAYER_RUN_SPEED = 9     # бег (зажатый Shift)
PLAYER_JUMP_POWER = -12
GRAVITY = 1.2

# Прозрачность передних слоёв
FOREGROUND_ALPHA_FADED = 0
FOREGROUND_ALPHA_VISIBLE = 255

# Клавиша для вызова меню паузы
PAUSE_KEY = pygame.K_ESCAPE   # или pygame.K_p

# --- Настройки спрайт-листа персонажа ---
PLAYER_FRAME_WIDTH = 32
PLAYER_FRAME_HEIGHT = 70

PLAYER_ANIMATIONS_CONFIG = {
    'idle':   {'filename': 'Idle',   'frames': 6, 'speed': 150},
    'walk':   {'filename': 'Walk',   'frames': 10, 'speed': 120},
    'run':    {'filename': 'Run',    'frames': 10, 'speed': 100},
    'attack': {'filename': 'Attack', 'frames': 4, 'speed': 100},
    'jump':   {'filename': 'Jump',   'frames': 5, 'speed': 250}
}