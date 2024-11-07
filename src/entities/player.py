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
        self.is_jump = False
        
        # Состояния
        self.facing_right = True
        self.is_big = False
        self.is_invincible = False
        self.current_animation = 'idle'
        self.animation_frame = 0

        # Переменные измерений
        self.PLAYER_SPEED = 2
        self.PLAYER_JUMP_POWER = 0.7
        self.PLAYER_JUMP_HEIGHT = 50
        self.PLAYER_POSITION = None

        self.GRAVITY = 0.6
        
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
        if not self.on_ground and not self.is_jump:
            self.apply_gravity()
        self.handle_movement()
        self.animate()
        
    def handle_movement(self):
        keys = pygame.key.get_pressed()
        
        # Горизонтальное движение
        self.velocity_x = 0

        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.PLAYER_SPEED
            self.facing_right = True
            
        # Прыжок
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.PLAYER_JUMP_POWER
            self.PLAYER_POSITION = 0
            self.is_jump = True
            self.on_ground = False

        if self.is_jump and self.PLAYER_JUMP_HEIGHT > self.PLAYER_POSITION:
            self.velocity_y += self.PLAYER_JUMP_POWER
            self.rect.y -= self.velocity_y
            self.PLAYER_POSITION += self.velocity_y
            print("***********", self.PLAYER_JUMP_HEIGHT, self.PLAYER_POSITION)
        else:
            self.is_jump = False
            print(self.is_jump)

        self.rect.x += self.velocity_x
        self.rect.y -= self.velocity_y

    def apply_gravity(self):
        self.velocity_y += self.GRAVITY
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