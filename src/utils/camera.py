import pygame

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        return entity.rect.move(self.camera_rect.topleft)

    def update(self, target):
        x = -target.rect.centerx + self.camera_rect.width // 2
        y = -target.rect.centery + self.camera_rect.height // 2
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.map_width - self.camera_rect.width), x)
        y = max(-(self.map_height - self.camera_rect.height), y)
        self.camera_rect = pygame.Rect(x, y, self.camera_rect.width, self.camera_rect.height)