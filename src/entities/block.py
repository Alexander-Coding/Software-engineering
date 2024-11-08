import pygame
from src.config import *


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type, image_path):
        super().__init__()
        print(f"Создание блока на {x}, {y}")
        self.block_type = block_type
        self.image_path = image_path
        self.load_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.has_coin = block_type == 'question'
        self.is_broken = False
        
    def load_sprite(self):
        # Временно создаем прямоугольник
        self.image = pygame.Surface((32, 32))

        if self.block_type == 'question':
            self.image.fill((255, 200, 0))

        else:
            self.image = pygame.image.load(str(self.image_path))
            
    def hit(self):
        if self.block_type == 'question' and self.has_coin:
            self.has_coin = False

            return True
        
        elif self.block_type == 'brick':
            self.is_broken = True
            self.kill()

        return False