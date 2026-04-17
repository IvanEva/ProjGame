import pygame
from settings import GRAVITY, PLAYER_JUMP_POWER, BLUE

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

    def update_animation(self):
        now = pygame.time.get_ticks()
        speed = self.animation_speeds.get(self.current_action, 100)
        if now - self.last_update > speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_action])
            self.image = self.animations[self.current_action][self.current_frame]

    def update(self, blocks):
        # Смена анимации
        if not self.on_ground:
            self.current_action = 'jump' if 'jump' in self.animations else 'idle'
        elif self.vel_x != 0:
            self.current_action = 'run' if 'run' in self.animations else 'walk'
        else:
            self.current_action = 'idle'

        # Защита от отсутствия анимации
        if self.current_action not in self.animations:
            self.current_action = 'idle'

        if self.current_frame >= len(self.animations[self.current_action]):
            self.current_frame = 0
        self.update_animation()

        # Движение
        self.rect.x += self.vel_x
        self.collide(self.vel_x, 0, blocks)

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False
        self.collide(0, self.vel_y, blocks)

        # Поворот
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