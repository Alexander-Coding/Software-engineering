import math
import pygame
from src.entities.enemy import Enemy


class Koopa(Enemy):
    def __init__(self, x, y, variant='green', behavior='walking'):
        """
        variant: 'green', 'red', 'blue'
        behavior: 'walking', 'flying', 'shell'
        """
        super().__init__(x, y, variant)
        self.behavior = behavior
        self.velocity_x = 2
        self.animation_speed = 0.15
        self.direction = -1
        
        # Параметры поведения
        self.is_shell_mode = behavior == 'shell'
        self.shell_speed = 8
        self.flying_height = 100  # Высота полета для летающих Koopa
        self.initial_y = y
        self.fly_offset = 0
        
        # Состояния
        self.is_kicked = False
        self.wake_up_timer = 0
        self.wake_up_delay = 5000  # 5 секунд до выхода из панциря

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
                pygame.image.load(path).convert_alpha() 
                for path in sprite_paths[self.variant]['walk']
            ],
            'shell': [
                pygame.image.load(path).convert_alpha() 
                for path in sprite_paths[self.variant]['shell']
            ],
            'shell_wake': [
                pygame.image.load(path).convert_alpha() 
                for path in sprite_paths[self.variant]['shell_wake']
            ],
            'fly': [
                pygame.image.load(path).convert_alpha() 
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
        if self.is_shell_mode:
            self.update_shell_state()

        else:
            self.update_normal_state()

        super().update()
        

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
        
        if self.is_kicked:
            self.current_animation = 'shell'
        else:
            if current_time - self.wake_up_timer > self.wake_up_delay:
                self.current_animation = 'shell_wake'

                if self.animation_frame >= len(self.sprites['shell_wake']) - 1:
                    self.exit_shell()
            else:
                self.current_animation = 'shell'
                

    def walk_movement(self):
        self.rect.x += self.velocity_x * self.direction
        

    def fly_movement(self):
        self.fly_offset += 0.05
        self.rect.x += self.velocity_x * self.direction
        self.rect.y = self.initial_y + math.sin(self.fly_offset) * self.flying_height
        

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
        

    def kick_shell(self, direction):
        if self.is_shell_mode:
            self.is_kicked = True
            self.velocity_x = self.shell_speed
            self.direction = direction
            self.wake_up_timer = pygame.time.get_ticks()  # Сбрасываем таймер
            

    def stomp(self):
        """Вызывается когда игрок прыгает на Koopa"""
        if not self.is_shell_mode:
            self.enter_shell()

        elif not self.is_kicked:
            self.kick_shell(1 if self.rect.x < self.get_player_position()[0] else -1)
            

    def check_collisions(self):
        # Проверка столкновений с блоками
        blocks_hit = pygame.sprite.spritecollide(self, self.game.current_scene.blocks, False)

        for block in blocks_hit:
            if self.velocity_x > 0:
                self.rect.right = block.rect.left
                self.reverse_direction()

            elif self.velocity_x < 0:
                self.rect.left = block.rect.right
                self.reverse_direction()