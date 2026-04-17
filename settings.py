import os

# Корневая директория проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Пути к ресурсам
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
BACKGROUNDS_DIR = os.path.join(IMAGES_DIR, 'backgrounds')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
LEVELS_DIR = os.path.join(ASSETS_DIR, 'levels')

# Фоновое изображение (если есть)
BACKGROUND_IMAGE = os.path.join(BACKGROUNDS_DIR, 'background.png')

# Разрешение (логическое)
LOGICAL_WIDTH = 1920
LOGICAL_HEIGHT = 1080

# Прозрачность передних слоёв (0 - полностью прозрачный, 255 - полностью непрозрачный)
FOREGROUND_ALPHA_FADED = 0    # или 0 для полной прозрачности
FOREGROUND_ALPHA_VISIBLE = 255

# Режим экрана
FULLSCREEN = True          # полноэкранный режим
SCALED = True              # масштабирование под реальное разрешение монитора
FPS = 30
TITLE = "Platformer Game"

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)

# Физика
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = -12
GRAVITY = 0.5