import pygame
from src.config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game

        self.tick = pygame.time.Clock().tick(60)

        self.is_big = self.game.game_state.mario_is_big

        self.x = x
        self.y = y

        if self.is_big:
            self.rect = None
            self.load_big_sprites()
        else:
            self.load_sprites()
        
        # Физика
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        
        # Состояния
        self.facing_right = True
        
        self.is_invincible = False
        self.current_animation = 'idle'
        self.animation_frame = 0

        # Переменные измерений
        self.PLAYER_SPEED = 180
        self.PLAYER_JUMP_POWER = 8
        self.GRAVITY = 15

        self.is_big = False  # Флаг для отслеживания размера игрока

        self.blocks = pygame.sprite.Group()
        
    def load_sprites(self, is_big=False):
        self.sprites = {
            'idle': [
                pygame.image.load(f'assets/images/characters/mario/small/idle.png')
            ],
            'run': [
                pygame.image.load(f'assets/images/characters/mario/small/run1.png'),
                pygame.image.load(f'assets/images/characters/mario/small/run2.png'),
                pygame.image.load(f'assets/images/characters/mario/small/run3.png')
            ],
            'jump': [
                pygame.image.load(f'assets/images/characters/mario/small/jump.png')
            ],
            'fall': [
                pygame.image.load(f'assets/images/characters/mario/small/death.png')
            ]
        }

        self.image = self.sprites['idle'][0]

        new_surface = pygame.Surface((self.image.get_width() - 12, self.image.get_height()))
        new_surface.blit(self.image, (0, 0), (0, 0, self.image.get_width() - 12, self.image.get_height()))

        self.image = new_surface

        if is_big:
            x = self.rect.x
            y = self.rect.y

        else:
            y = self.y
            x = self.x

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        

    def load_big_sprites(self):
        self.sprites = {
            'idle': [
                pygame.transform.scale(pygame.image.load(f'assets/images/characters/mario/big/idle.png'), (32, 64))
            ],
            'run': [
                pygame.transform.scale(pygame.image.load(f'assets/images/characters/mario/big/run1.png'), (32, 64)),
                pygame.transform.scale(pygame.image.load(f'assets/images/characters/mario/big/run2.png'), (32, 64)),
                pygame.transform.scale(pygame.image.load(f'assets/images/characters/mario/big/run3.png'), (32, 64))
                
            ],
            'jump': [
                pygame.transform.scale(pygame.image.load(f'assets/images/characters/mario/big/jump.png'), (32, 64))
                
            ],
            'fall': [
                pygame.transform.scale(pygame.image.load(f'assets/images/characters/mario/big/death.png'), (32, 64))
                
            ]
        }

        if not self.rect:
            y = self.y
            x = self.x

        else:
            y = self.rect.y
            x = self.rect.x
        
        self.image = self.sprites['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 32


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


    def increase_size(self):
        if not self.is_big:
            self.is_big = True
            self.game.game_state.mario_is_big = True
            self.load_big_sprites()

    def reducing_size(self):
        if self.is_big:
            self.is_big = False
            self.game.game_state.mario_is_big = False
            self.load_sprites(True)
