import pygame
from src.config import *
from src.utils.asset_loader import AssetLoader


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.tick = pygame.time.Clock().tick(60)

        self.load_sprites()
        self.image = self.sprites['idle'][0]
        self.image = pygame.transform.scale(self.image, (24, 32))
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

        # Переменные измерений
        self.PLAYER_SPEED = 180
        self.PLAYER_JUMP_POWER = 6
        self.GRAVITY = 10

        self.blocks = pygame.sprite.Group()
        
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
        if not self.on_ground:
            self.apply_gravity()
        self.handle_movement()
        self.animate()

    def handle_movement(self):
        keys = pygame.key.get_pressed()

        # Горизонтальное движение
        self.velocity_x = 0

        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.PLAYER_SPEED * (self.tick/1000)
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = self.PLAYER_SPEED * (self.tick/1000)
            self.facing_right = True

        # Прыжок
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity_y -= self.PLAYER_JUMP_POWER
            self.on_ground = False

        # Проверка столкновений с блоками
        for block in self.blocks:
            # Проверка столкновения по оси X
            if block.rect.colliderect(self.rect.move(self.velocity_x, 0)):
                self.velocity_x = 0

            # Проверка столкновения по оси Y
            if block.rect.colliderect(self.rect.move(0, self.velocity_y)):
                if self.velocity_y > 0:  # Падение
                    self.rect.bottom = block.rect.top  # Устанавливаем игрока на верх блока
                    self.velocity_y = 0
                    self.on_ground = True  # Игрок на земле
                elif self.velocity_y < 0:  # Подъем (прыжок)
                    self.rect.top = block.rect.bottom  # Устанавливаем игрока на низ блока
                    self.velocity_y = 0
                    block.break_block()
                    
        if not self.handle_collision():
            self.on_ground = False

        # Обновляем позицию игрока
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def handle_collision(self):
        """Проверяет, стоит ли персонаж на платформе."""
        for block in self.blocks:
            if block.rect.colliderect(self.rect.move(0, 1)):  # Проверяем, есть ли коллизия с блоком чуть ниже персонажа
                return True
        return False

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += self.GRAVITY * (self.tick/1000) # Применяем гравитацию к вертикальной скорости
            if self.velocity_y > 5:
                self.velocity_y = 5

    def animate(self):
        if not self.on_ground:
            self.current_animation = 'jump' if self.velocity_y < 0 else 'fall'
        else:
            self.current_animation = 'run' if self.velocity_x != 0 else 'idle'
            
        self.animation_frame = (self.animation_frame + 0.2) % len(self.sprites[self.current_animation])
        self.image = self.sprites[self.current_animation][int(self.animation_frame)]
        
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)