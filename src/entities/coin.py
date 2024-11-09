import pygame
from src.config import *


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.load_sprites()
        self.image = self.sprites[1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = player
        self.animation_frame = 0


    @staticmethod
    def get_image():
        return pygame.image.load('assets/images/items/coin/coin_spin_2.png')
    

    @staticmethod
    def get_image_path():
        return 'assets/images/items/coin/coin_spin_2.png'
        

    def load_sprites(self):
        self.sprites = [
            pygame.image.load('assets/images/items/coin/coin_spin_1.png'),
            pygame.image.load('assets/images/items/coin/coin_spin_2.png'),
            pygame.image.load('assets/images/items/coin/coin_spin_3.png')
        ]
        
    def update(self):
        self.animate()
        
    def animate(self):
        self.animation_frame = (self.animation_frame + 0.1) % len(self.sprites)
        self.image = self.sprites[int(self.animation_frame)]
        
    def collect(self, scoring_system):
        scoring_system.add_coins()
        scoring_system.add_score('coin')
        self.kill()