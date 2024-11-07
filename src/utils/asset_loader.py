import os
import pygame
from src.config import ASSETS_DIR

class AssetLoader:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.music = {}
        self.load_assets()
        self.a = self.images
    
    def load_assets(self):
        # Загрузка изображений
        self._load_directory(os.path.join(ASSETS_DIR, "images"), self.images, pygame.image.load)
        
        # Загрузка звуков
        self._load_directory(os.path.join(ASSETS_DIR, "sounds"), self.sounds, pygame.mixer.Sound)
        
        # Загрузка музыки
        self._load_directory(os.path.join(ASSETS_DIR, "music"), self.music, lambda x: x)

    
    def _load_directory(self, directory, storage_dict, loader_func):
        TILE_SIZE = 32  # Укажите здесь размер вашей клетки уровня
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.png', '.jpg', '.wav', '.mp3')):
                    path = os.path.join(root, file)
                    key = os.path.splitext(file)[0]
                    try:
                        if file.endswith(('.png', '.jpg')):
                            loaded_asset = loader_func(path).convert_alpha()
                            trimmed_asset = self._trim_transparent(loaded_asset)
                            # Масштабируем изображение до размера клетки
                            storage_dict[key] = pygame.transform.scale(trimmed_asset, (TILE_SIZE, TILE_SIZE))
                        else:
                            storage_dict[key] = loader_func(path)
                    except pygame.error:
                        print(f"Ошибка загрузки файла: {path}")

    def _trim_transparent(self, surface):
        # Получаем маску непрозрачных пикселей
        mask = pygame.mask.from_surface(surface)
        if mask.count() == 0:  # Если изображение полностью прозрачное
            return surface
            
        # Находим границы непрозрачной области
        bounds = mask.get_bounding_rects()[0]
        
        # Создаем новую поверхность с обрезанным изображением
        new_surface = pygame.Surface(bounds.size, pygame.SRCALPHA)
        new_surface.blit(surface, (0, 0), bounds)
        
        return new_surface
