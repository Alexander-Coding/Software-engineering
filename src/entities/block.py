import pygame
from src.config import *


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type, image_path):
        super().__init__()
        self.block_type = block_type
        self.image_path = image_path
        self.image = self.load_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.has_coin = block_type == 'question'
        self.is_broken = False
        
    def load_sprite(self):
        return pygame.image.load(str(self.image_path))