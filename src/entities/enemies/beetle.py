import pygame
from resource_path import resource_path
from src.entities.enemy import Enemy


class Beetle(Enemy):
    def __init__(self, x, y, player, game, blocks, variant='dark'):
        super().__init__(x, y, player, game, blocks, variant)
        self.velocity_x = 1.5
        self.animation_speed = 0.12
        self.is_shell_mode = False
        self.shell_speed = 8
        self.direction = -1

        self.enemy_name = f'beetle_{variant}'

        self.load_sprites()


    @classmethod
    def get_variants(cls):
        return [
            {
                'enemy_name': 'beetle_dark',
                'image_path': 'assets/images/enemies/beetle/beetle_dark/run_left1.png',
                'color': 'dark',
                'behavior': None
            }
        ]
        

    def load_sprites(self):
        sprite_paths = {
            'dark': {
                'walk_left': [
                    'assets/images/enemies/beetle/beetle_dark/run_left1.png',
                    'assets/images/enemies/beetle/beetle_dark/run_left2.png'
                ],
                'walk_right': [
                    'assets/images/enemies/beetle/beetle_dark/run_right1.png',
                    'assets/images/enemies/beetle/beetle_dark/run_right2.png'
                ],
                'shell': ['assets/images/enemies/beetle/beetle_dark/shell.png']
            }
        }
        
        self.sprites = {
            'walk_left': [
                pygame.image.load(resource_path(path)).convert_alpha() 
                for path in sprite_paths[self.variant]['walk_left']
            ],
            'walk_right': [
                pygame.image.load(resource_path(path)).convert_alpha() 
                for path in sprite_paths[self.variant]['walk_right']
            ],
            'shell': [
                pygame.image.load(resource_path(path)).convert_alpha() 
                for path in sprite_paths[self.variant]['shell']
            ]
        }

        self.image = self.sprites['walk_left'][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Начальная анимация в зависимости от направления
        self.current_animation = 'walk_left'
        

    def update(self):
        if not self.is_shell_mode:
            # Обновляем анимацию в зависимости от направления
            self.current_animation = 'walk_left' if self.direction == -1 else 'walk_right'
            
        super().update()
        

    def enter_shell_mode(self):
        self.is_shell_mode = True
        self.current_animation = 'shell'
        self.velocity_x = 0
        self.can_be_stomped = False
        

    def kick_shell(self, direction):
        if self.is_shell_mode:
            self.velocity_x = self.shell_speed
            self.direction = direction
            

    def reverse_direction(self):
        self.direction *= -1
        self.current_animation = 'walk_left' if self.direction == -1 else 'walk_right'