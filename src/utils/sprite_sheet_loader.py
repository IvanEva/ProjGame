import os
import pygame
from settings import PLAYER_FRAME_WIDTH, PLAYER_FRAME_HEIGHT

def load_animation_from_sheet(file_path, frame_width, frame_height, num_frames, convert_alpha=True):
    try:
        sheet = pygame.image.load(file_path)
        if convert_alpha:
            sheet = sheet.convert_alpha()
    except pygame.error as e:
        print(f"Ошибка загрузки {file_path}: {e}")
        return []

    sheet_width, sheet_height = sheet.get_size()
    frames = []
    for i in range(num_frames):
        rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        if rect.right > sheet_width or rect.bottom > sheet_height:
            print(f"Ошибка: кадр {i} выходит за границы {file_path} ({sheet_width}x{sheet_height})")
            break
        frame = sheet.subsurface(rect).copy()
        frames.append(frame)
    return frames

def load_all_animations(animations_dir, config):
    animations = {}
    speeds = {}
    for action, params in config.items():
        filename = params.get('filename')
        num_frames = params.get('frames', 0)
        if not filename or num_frames == 0:
            continue
        speed = params.get('speed', 100)
        file_path = os.path.join(animations_dir, f"{filename}.png")
        frames = load_animation_from_sheet(file_path, PLAYER_FRAME_WIDTH, PLAYER_FRAME_HEIGHT, num_frames)
        if frames:
            animations[action] = frames
            speeds[action] = speed
            print(f"Загружена анимация {action}: {len(frames)} кадров")
        else:
            print(f"Не удалось загрузить {action} из {file_path}")
    return animations, speeds
