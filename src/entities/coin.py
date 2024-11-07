import pygame
from src.config import *


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_sprites()
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_frame = 0
        
    def load_sprites(self):
        self.sprites = []  # Загрузка спрайтов из asset_loader
        
    def update(self):
        self.animate()
        
    def animate(self):
        self.animation_frame = (self.animation_frame + 0.2) % len(self.sprites)
        self.image = self.sprites[int(self.animation_frame)]
        
    def collect(self, scoring_system):
        scoring_system.add_coins()
        scoring_system.add_score('coin')
        self.kill()