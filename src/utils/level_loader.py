import os
import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from settings import LEVELS_DIR, PLAYER_ANIMATIONS_DIR, PLAYER_ANIMATIONS_CONFIG
from src.entities.block import Block
from src.entities.player import Player
from src.utils.sprite_sheet_loader import load_all_animations

def load_level(tmx_filename, player_group, blocks_group, all_sprites, foreground_group):
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

    def get_tile_image(gid):
        if gid == 0:
            return None
        if hasattr(tmx_data, 'get_tile_image_by_gid'):
            img = tmx_data.get_tile_image_by_gid(gid)
        elif hasattr(tmx_data, 'get_tile_image'):
            img = tmx_data.get_tile_image(gid)
        else:
            return None
        if img is None:
            return None
        if img.get_alpha() is None:
            img = img.convert_alpha()
        return img

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            print(f"  Слой: {layer.name} (тайловый)")
            for x, y, gid in layer:
                if gid == 0:
                    continue
                pixel_x = x * tile_w
                pixel_y = y * tile_h
                tile_image = get_tile_image(gid)
                if tile_image is None:
                    continue

                if layer.name == "Platforms":
                    tile_props = tmx_data.get_tile_properties_by_gid(gid) or {}
                    is_one_way = tile_props.get("one_way", False)
                    block = Block(pixel_x, pixel_y, tile_w, tile_h, is_one_way)
                    block.image = tile_image
                    blocks_group.add(block)
                    all_sprites.add(block)

                elif layer.name.startswith("Front"):
                    sprite = pygame.sprite.Sprite()
                    sprite.image = tile_image.copy()
                    sprite.rect = tile_image.get_rect(topleft=(pixel_x, pixel_y))
                    sprite.layer_name = layer.name
                    sprite.original_image = tile_image
                    all_sprites.add(sprite)
                    foreground_group.add(sprite)

                else:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = tile_image
                    sprite.rect = tile_image.get_rect(topleft=(pixel_x, pixel_y))
                    all_sprites.add(sprite)

        elif isinstance(layer, pytmx.TiledObjectGroup):
            print(f"  Слой объектов: {layer.name}")
            if layer.name == "Entities":
                for obj in layer:
                    if obj.name == "player":
                        player = Player(0, 0)
                        animations, speeds = load_all_animations(PLAYER_ANIMATIONS_DIR, PLAYER_ANIMATIONS_CONFIG)
                        if animations:
                            player.load_animations(animations, speeds)
                        else:
                            print("⚠️ Анимации не загружены, используется заглушка")
                        player.rect.bottom = obj.y + obj.height
                        player.rect.x = obj.x
                        player_group.add(player)
                        all_sprites.add(player)

    return map_width, map_height