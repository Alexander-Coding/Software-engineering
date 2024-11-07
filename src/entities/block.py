import pygame
import sys
sys.path.append(r'C:\Users\Alexa\github\BioSense\mario\src')
from config import *

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type='ground'):
        super().__init__()
        print(f"Создание блока на {x}, {y}")
        self.block_type = block_type
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
            self.image.fill((139, 69, 19))
            
    def hit(self):
        if self.block_type == 'question' and self.has_coin:
            self.has_coin = False

            return True
        
        elif self.block_type == 'brick':
            self.is_broken = True
            self.kill()

        return False