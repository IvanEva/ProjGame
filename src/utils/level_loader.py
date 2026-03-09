import os
import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from settings import LEVELS_DIR
from src.entities.block import Block
from src.entities.player import Player

def load_level(tmx_filename, player_group, blocks_group, all_sprites):
    map_path = os.path.join(LEVELS_DIR, tmx_filename)
    print(f"🔍 Загрузка уровня из: {map_path}")  # отладочный вывод

    if not os.path.exists(map_path):
        print(f"❌ Файл не существует: {map_path}")
        return 0, 0

    try:
        tmx_data = load_pygame(map_path)
        print("✅ Карта успешно загружена")
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return 0, 0

    tile_w = tmx_data.tilewidth
    tile_h = tmx_data.tileheight
    map_width = tmx_data.width * tile_w
    map_height = tmx_data.height * tile_h

    # Обработка тайловых слоёв
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            print(f"  Слой: {layer.name} (тайловый)")  # отладка
            for x, y, image in layer.tiles():
                if image is None:
                    continue
                pixel_x = x * tile_w
                pixel_y = y * tile_h

                if layer.name == "Platforms":
                    # Твёрдый слой
                    block = Block(pixel_x, pixel_y, tile_w, tile_h)
                    block.image = image
                    blocks_group.add(block)
                    all_sprites.add(block)
                else:
                    # Декоративный слой
                    sprite = pygame.sprite.Sprite()
                    sprite.image = image
                    sprite.rect = image.get_rect(topleft=(pixel_x, pixel_y))
                    all_sprites.add(sprite)

        elif isinstance(layer, pytmx.TiledObjectGroup):
            print(f"  Слой объектов: {layer.name}")  # отладка
            if layer.name == "Entities":
                for obj in layer:
                    print(f"    Объект: {obj.name}, позиция ({obj.x}, {obj.y})")  # отладка
                    if obj.name == "player":
                        # Учтите, что в Tiled объекты могут иметь ширину/высоту,
                        # но для спавна игрока обычно достаточно точки.
                        player = Player(obj.x, obj.y)
                        player_group.add(player)
                        all_sprites.add(player)
                    # Добавьте другие объекты по необходимости

    return map_width, map_height