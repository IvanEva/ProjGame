import pygame
from settings import GRAVITY, PLAYER_JUMP_POWER, PLAYER_SPEED, PLAYER_RUN_SPEED, BLUE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Заглушка (будет заменена при вызове load_animations)
        self.animations = {
            'idle': [self._create_fallback_surface()],
            'walk': [self._create_fallback_surface()],
            'run': [self._create_fallback_surface()],
            'attack': [self._create_fallback_surface()],
        }
        self.animation_speeds = {'idle': 100, 'walk': 100, 'run': 100, 'attack': 100}
        self.current_action = 'idle'
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

        self.image = self.animations[self.current_action][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.is_running = False

    def _create_fallback_surface(self):
        surf = pygame.Surface((30, 50))
        surf.fill(BLUE)
        return surf

    def load_animations(self, animations, speeds=None):
        if animations:
            self.animations = animations
            if speeds:
                self.animation_speeds = speeds
            else:
                for action in animations:
                    self.animation_speeds[action] = 100
            self.current_action = 'idle'
            self.current_frame = 0
            self.image = self.animations[self.current_action][self.current_frame]
            # Обновляем размер rect, сохраняя нижнюю границу
            old_bottom = self.rect.bottom
            self.rect.size = self.image.get_size()
            self.rect.bottom = old_bottom

    def update_animation(self):
        now = pygame.time.get_ticks()
        speed = self.animation_speeds.get(self.current_action, 100)
        if now - self.last_update > speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_action])
            new_image = self.animations[self.current_action][self.current_frame]
            old_bottom = self.rect.bottom
            self.image = new_image
            self.rect.size = new_image.get_size()
            self.rect.bottom = old_bottom

    def update(self, blocks):
        keys = pygame.key.get_pressed()
        # Бег: зажатый Shift
        self.is_running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        # Выбор скорости
        if self.is_running and self.on_ground:
            current_speed = PLAYER_RUN_SPEED
        else:
            current_speed = PLAYER_SPEED

        # Горизонтальное управление
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -current_speed
        if keys[pygame.K_RIGHT]:
            self.vel_x = current_speed

        # Смена анимации
        if not self.on_ground:
            self.current_action = 'jump' if 'jump' in self.animations else 'idle'
        elif self.vel_x != 0:
            if self.is_running and 'run' in self.animations:
                self.current_action = 'run'
            else:
                self.current_action = 'walk' if 'walk' in self.animations else 'idle'
        else:
            self.current_action = 'idle'

        # Защита от отсутствия анимации
        if self.current_action not in self.animations:
            self.current_action = 'idle'

        if self.current_frame >= len(self.animations[self.current_action]):
            self.current_frame = 0
        self.update_animation()

        # Движение и коллизии
        self.rect.x += self.vel_x
        self.collide(self.vel_x, 0, blocks)

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False
        self.collide(0, self.vel_y, blocks)

        # Поворот спрайта
        if self.vel_x > 0:
            self.facing_right = True
        elif self.vel_x < 0:
            self.facing_right = False

        frame = self.animations[self.current_action][self.current_frame]
        if self.facing_right:
            self.image = frame
        else:
            self.image = pygame.transform.flip(frame, True, False)

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