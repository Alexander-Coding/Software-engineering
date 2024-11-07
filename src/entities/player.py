import pygame
from src.config import *
from src.utils.asset_loader import AssetLoader

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_sprites()
        self.image = self.sprites['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Физика
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        
        # Состояния
        self.facing_right = True
        self.is_big = False
        self.is_invincible = False
        self.current_animation = 'idle'
        self.animation_frame = 0
        
    def load_sprites(self):
        self.sprites = {
            'idle': [
                pygame.image.load('assets/images/characters/mario/small/idle.png').convert_alpha()
            ],
            'run': [
                pygame.image.load('assets/images/characters/mario/small/run1.png').convert_alpha(),
                pygame.image.load('assets/images/characters/mario/small/run2.png').convert_alpha(),
                pygame.image.load('assets/images/characters/mario/small/run3.png').convert_alpha()
            ],
            'jump': [
                pygame.image.load('assets/images/characters/mario/small/jump.png').convert_alpha()
            ],
            'fall': [
                pygame.image.load('assets/images/characters/mario/small/death.png').convert_alpha()
            ]
        }
        
        # Устанавливаем начальный спрайт
        self.image = self.sprites['idle'][0]
        self.rect = self.image.get_rect()
    
    def update(self):
        self.apply_gravity()
        self.handle_movement()
        self.animate()
        
    def handle_movement(self):
        keys = pygame.key.get_pressed()
        
        # Горизонтальное движение
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True
            
        # Прыжок
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = PLAYER_JUMP_POWER
            self.on_ground = False
            
        self.rect.x += self.velocity_x
        
    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
    def animate(self):
        if not self.on_ground:
            self.current_animation = 'jump' if self.velocity_y < 0 else 'fall'
        else:
            self.current_animation = 'run' if self.velocity_x != 0 else 'idle'
            
        self.animation_frame = (self.animation_frame + 0.2) % len(self.sprites[self.current_animation])
        self.image = self.sprites[self.current_animation][int(self.animation_frame)]
        
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)