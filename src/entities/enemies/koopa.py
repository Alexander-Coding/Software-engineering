import math
import pygame
from resource_path import resource_path
from src.entities.enemy import Enemy
from src.config import *


class Koopa(Enemy):
    def __init__(self, x, y, player, game, blocks, variant='green', behavior='walking'):
        """
        variant: 'green', 'red', 'blue'
        behavior: 'walking', 'flying', 'shell'
        """
        super().__init__(x, y, player, game, blocks, variant)
        self.behavior = behavior
        self.velocity_x = 0.5
        self.animation_speed = 0.15
        self.direction = -1
        
        # Параметры поведения
        self.is_shell_mode = behavior == 'shell'
        self.shell_speed = 10
        self.flying_height = 100  # Высота полета для летающих Koopa
        self.initial_y = y
        self.fly_offset = 0

        # Состояния
        self.is_kicked = False
        self.wake_up_timer = 0
        self.wake_up_delay = 5000  # 5 секунд до выхода из панциря

        # Тайминг
        self.reverse_interval = 500
        self.attack_time = pygame.time.get_ticks()
        self.last_reverse_time = pygame.time.get_ticks()

        self.enemy_name = f'koopa_{variant}_{behavior}'

        self.load_sprites()


    @classmethod
    def get_variants(cls):
        return [
            {
                'enemy_name': 'koopa_walking_green',
                'image_path': 'assets/images/enemies/koopas/koopa_green/run1.png',
                'color': 'green',
                'behavior': 'walking'
            },
            {
                'enemy_name': 'koopa_walking_red',
                'image_path': 'assets/images/enemies/koopas/koopa_red/run1.png',
                'color': 'red',
                'behavior': 'walking'
            },
            {
                'enemy_name': 'koopa_walking_blue',
                'image_path': 'assets/images/enemies/koopas/koopa_blue/run1.png',
                'color': 'blue',
                'behavior': 'walking'
            },
            {
                'enemy_name': 'koopa_flying_green',
                'image_path': 'assets/images/enemies/koopas/koopa_green/fly1.png',
                'color': 'green',
                'behavior': 'flying'
            },
            {
                'enemy_name': 'koopa_flying_red',
                'image_path': 'assets/images/enemies/koopas/koopa_red/fly1.png',
                'color': 'red',
                'behavior': 'flying'
            },
            {
                'enemy_name': 'koopa_flying_blue',
                'image_path': 'assets/images/enemies/koopas/koopa_blue/fly1.png',
                'color': 'blue',
                'behavior': 'flying'
            }
        ]

    def load_sprites(self):
        sprite_paths = {
            'green': {
                'walk': [
                    'assets/images/enemies/koopas/koopa_green/run1.png',
                    'assets/images/enemies/koopas/koopa_green/run2.png'
                ],
                'shell': [
                    'assets/images/enemies/koopas/koopa_green/death2.png'
                    ],
                'shell_wake': [
                    'assets/images/enemies/koopas/koopa_green/death1.png',
                    'assets/images/enemies/koopas/koopa_green/death2.png'
                ],
                'fly': [
                    'assets/images/enemies/koopas/koopa_green/fly1.png',
                    'assets/images/enemies/koopas/koopa_green/fly2.png'
                ],
            }, 
            'red': {
                'walk': [
                    'assets/images/enemies/koopas/koopa_red/run1.png',
                    'assets/images/enemies/koopas/koopa_red/run2.png'
                ],
                'shell': [
                    'assets/images/enemies/koopas/koopa_red/death2.png'
                    ],
                'shell_wake': [
                    'assets/images/enemies/koopas/koopa_red/death1.png',
                    'assets/images/enemies/koopas/koopa_red/death2.png'
                ],
                'fly': [
                    'assets/images/enemies/koopas/koopa_red/fly1.png',
                    'assets/images/enemies/koopas/koopa_red/fly2.png'
                ],
            },
            'blue': {
                'walk': [
                    'assets/images/enemies/koopas/koopa_blue/run1.png',
                    'assets/images/enemies/koopas/koopa_blue/run2.png'
                ],
                'shell': [
                    'assets/images/enemies/koopas/koopa_blue/death2.png'
                    ],
                'shell_wake': [
                    'assets/images/enemies/koopas/koopa_blue/death1.png',
                    'assets/images/enemies/koopas/koopa_blue/death2.png'
                ],
                'fly': [
                    'assets/images/enemies/koopas/koopa_blue/fly1.png',
                    'assets/images/enemies/koopas/koopa_blue/fly2.png'
                ],
            }
        }
        
        # Загружаем базовые спрайты
        self.sprites = {
            'walk': [
                pygame.image.load(resource_path(path)).convert_alpha() 
                for path in sprite_paths[self.variant]['walk']
            ],
            'shell': [
                pygame.image.load(resource_path(path)).convert_alpha() 
                for path in sprite_paths[self.variant]['shell']
            ],
            'shell_wake': [
                pygame.image.load(resource_path(path)).convert_alpha() 
                for path in sprite_paths[self.variant]['shell_wake']
            ],
            'fly': [
                pygame.image.load(resource_path(path)).convert_alpha() 
                for path in sprite_paths[self.variant]['fly']
            ]
        }

        if self.behavior == 'flying':
            self.image = self.sprites['fly'][0]
        
        else:
            self.image = self.sprites['walk'][0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.take_damage()
        self.update_shell_state()
        if not self.is_shell_mode:
            self.update_normal_state()
            self.attack()
        super().update()

    def attack(self):
        if self.curren - self.attack_time >= self.reverse_interval:
            if self.rect.colliderect(self.player.rect.move(1, 0)) or self.rect.colliderect(self.player.rect.move(-1, 0)):
                self.player.Death()

    def handle_collision(self):
        for block in self.blocks:
            if block.rect.colliderect(self.rect.move(0, 1)):
                return True
        return False

    def take_damage(self):
        self.curren = pygame.time.get_ticks()
            # Проверка на столкновение с верхней частью черепахи
        if self.rect.colliderect(self.player.rect.move(0, 1)):
            if self.curren - self.attack_time >= self.reverse_interval:
                self.attack_time = pygame.time.get_ticks()
                self.stomp()

    def update_normal_state(self):
        if self.behavior == 'flying':
            self.fly_movement()
            self.current_animation = 'fly'
        else:
            self.walk_movement()
            self.current_animation = 'walk'
            
        # Отражаем спрайт если движемся вправо
        if self.direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update_shell_state(self):
        current_time = pygame.time.get_ticks()

        if self.is_shell_mode:
            if current_time - self.wake_up_timer > self.wake_up_delay:
                self.current_animation = 'shell_wake'

                if self.animation_frame >= len(self.sprites['shell_wake']) - 1:
                    self.exit_shell()

    def walk_movement(self):
        self.velocity_x = 1
        self.current_time = pygame.time.get_ticks()

        for block in self.blocks:
            if block.rect.colliderect(self.rect.move(self.velocity_x, 0)):
                self.velocity_x = 0

                if self.current_time - self.last_reverse_time >= self.reverse_interval:
                    self.reverse_direction()
                    self.last_reverse_time = self.current_time
                    self.velocity_x = 1

            if block.rect.colliderect(self.rect.move(0, self.velocity_y)):
                if self.velocity_y > 0:  # Падение
                    self.rect.bottom = block.rect.top  # Устанавливаем игрока на верх блока
                    self.velocity_y = 0
                    self.on_ground = True  # Игрок на земле

                elif self.velocity_y < 0:  # Подъем (прыжок)
                    self.rect.top = block.rect.bottom  # Устанавливаем игрока на низ блока
                    self.velocity_y = 0

        if not self.handle_collision():
            self.on_ground = False

        self.rect.x += self.velocity_x * self.direction
        self.rect.y += self.velocity_y

    def fly_movement(self):
        self.fly_offset += 0.05
        self.velocity_x = 1
        self.current_time = pygame.time.get_ticks()

        self.velocity_y = math.sin(self.fly_offset) * 0.5
        new_y_position = self.initial_y + self.velocity_y * self.flying_height

        collision_y = False

        for block in self.blocks:
            if block.rect.colliderect(self.rect.move(0, new_y_position - self.rect.y)):
                collision_y = True  # Отмечаем, что произошло столкновение по Y

        if not collision_y:
            self.rect.y = new_y_position

    def enter_shell(self):
        self.is_shell_mode = True
        self.behavior = 'shell'
        self.current_animation = 'shell'
        self.velocity_x = 0
        self.wake_up_timer = pygame.time.get_ticks()

    def exit_shell(self):
        self.is_shell_mode = False
        self.behavior = 'walking'
        self.is_kicked = False
        self.velocity_x = 2
        self.on_ground = False

    def kick_shell(self, direction):
        if self.is_shell_mode:
            self.curren = pygame.time.get_ticks()
            # Проверка на столкновение с игроком
            if self.rect.colliderect(self.player.rect.move(1, 0)) or self.rect.colliderect(
                    self.player.rect.move(-1, 0) or self.is_kicked):
                # Проверка времени для атаки
                if self.curren - self.attack_time >= self.reverse_interval:
                    self.attack_time = pygame.time.get_ticks()  # Сбрасываем таймер атаки
                    self.is_kicked = True

                    # Устанавливаем скорость и направление движения черепахи
                    self.velocity_x = (self.shell_speed+40) * direction

                    # Обновляем направление черепахи
                    self.direction = direction

                    # Сбрасываем таймер пробуждения
                    self.wake_up_timer = pygame.time.get_ticks()

    def stomp(self):
        if self.behavior == "flying":
            self.behavior = "walking"
            self.player.kill_enemy()

        else:
            if not self.is_shell_mode:
                self.enter_shell()
                self.player.kill_enemy()

            else:
                if not self.is_kicked:
                    self.kick_shell(1 if self.rect.x < self.get_player_position()[0] else -1)
