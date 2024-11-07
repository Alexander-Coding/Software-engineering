import pygame
import sys
sys.path.append(r'C:\Users\Alexa\github\BioSense\mario\src')
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='goomba'):
        super().__init__()
        self.enemy_type = enemy_type
        self.load_sprites()
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.velocity_x = -2
        self.velocity_y = 0
        self.animation_frame = 0
        
    def load_sprites(self):
        self.sprites = []  # Загрузка спрайтов из asset_loader
        
    def update(self):
        self.apply_gravity()
        self.move()
        self.animate()
        
    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
    def move(self):
        self.rect.x += self.velocity_x
        
    def animate(self):
        self.animation_frame = (self.animation_frame + 0.1) % len(self.sprites)
        self.image = self.sprites[int(self.animation_frame)]
        
    def reverse_direction(self):
        self.velocity_x *= -1
        
    def die(self):
        self.kill()