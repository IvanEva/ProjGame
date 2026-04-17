import os
import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from settings import LEVELS_DIR
from src.entities.block import Block
from src.entities.player import Player

def load_level(tmx_filename, player_group, blocks_group, all_sprites, foreground_group):
    """
    Загружает карту из Tiled .tmx файла.
    Возвращает размер карты в пикселях (width, height).
    """
    map_path = os.path.join(LEVELS_DIR, tmx_filename)
    print(f"🔍 Загрузка уровня из: {map_path}")

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

    # Вспомогательная функция для получения изображения тайла по GID
    def get_tile_image(gid):
        """Возвращает поверхность pygame для тайла с указанным GID."""
        if gid == 0:
            return None
        # Пытаемся получить изображение через get_tile_image_by_gid
        if hasattr(tmx_data, 'get_tile_image_by_gid'):
            return tmx_data.get_tile_image_by_gid(gid)
        # Альтернативный способ: через get_tile_image (если метод существует)
        elif hasattr(tmx_data, 'get_tile_image'):
            return tmx_data.get_tile_image(gid)
        else:
            return None

    # Обработка тайловых слоёв
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            print(f"  Слой: {layer.name} (тайловый)")

            # Используем итератор, который возвращает кортежи (x, y, gid)
            for x, y, gid in layer:
                if gid == 0:  # GID=0 означает отсутствие тайла
                    continue

                pixel_x = x * tile_w
                pixel_y = y * tile_h

                # Получаем изображение тайла по GID
                tile_image = get_tile_image(gid)
                if tile_image is None:
                    continue

                # --- Слой платформ (с коллизией) ---
                if layer.name == "Platforms":
                    # Получаем свойства тайла по GID
                    tile_props = tmx_data.get_tile_properties_by_gid(gid) if gid else {}
                    is_one_way = tile_props.get("one_way", False) if tile_props else False

                    block = Block(pixel_x, pixel_y, tile_w, tile_h, is_one_way)
                    block.image = tile_image
                    blocks_group.add(block)
                    all_sprites.add(block)

                # --- Передние слои (front1..front5) ---
                elif layer.name.startswith("Front"):
                    sprite = pygame.sprite.Sprite()
                    sprite.image = tile_image.copy()
                    sprite.rect = tile_image.get_rect(topleft=(pixel_x, pixel_y))
                    sprite.layer_name = layer.name  # запоминаем, из какого слоя этот спрайт
                    sprite.original_image = tile_image
                    all_sprites.add(sprite)
                    foreground_group.add(sprite)

                # --- Остальные декоративные слои (фон, задний план) ---
                else:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = tile_image
                    sprite.rect = tile_image.get_rect(topleft=(pixel_x, pixel_y))
                    all_sprites.add(sprite)

        # Обработка объектных слоёв
        elif isinstance(layer, pytmx.TiledObjectGroup):
            print(f"  Слой объектов: {layer.name}")
            if layer.name == "Entities":
                for obj in layer:
                    print(f"    Объект: {obj.name}, позиция ({obj.x}, {obj.y})")
                    if obj.name == "player":
                        # Корректируем y, чтобы игрок стоял ногами на тайле
                        player = Player(obj.x, obj.y - 50)
                        player_group.add(player)
                        all_sprites.add(player)
                    # Здесь можно добавить других объектов (enemy, bonus и т.д.)

    return map_width, map_height