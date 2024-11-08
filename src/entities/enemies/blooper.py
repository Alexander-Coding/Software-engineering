import math
import pygame
from src.entities.enemy import Enemy


class Blooper(Enemy):
    def __init__(self, x, y, variant='dark'):
        super().__init__(x, y, variant)
        self.animation_speed = 0.15
        self.swim_speed = 3
        self.chase_distance = 200
        self.wave_offset = 0
        self.can_be_stomped = False

        self.enemy_name = f'blooper_{variant}'
        
        self.load_sprites()


    @classmethod
    def get_variants(cls):
        return [
            {
                'enemy_name': 'blooper_dark',
                'image_path': 'assets/images/enemies/bloopa/run1.png',
                'color': 'dark',
                'behavior': None
            }
        ]


    def load_sprites(self):
        sprite_paths = {
            'dark': {
                'swim': [
                    'assets/images/enemies/bloopa/run1.png', 
                    'assets/images/enemies/bloopa/run2.png'
                    ],
                'chase': [
                    'assets/images/enemies/bloopa/run2.png'
                    ]
            }
        }
        
        self.sprites = {
            'swim': [pygame.image.load(path).convert_alpha() for path in sprite_paths[self.variant]['swim']],
            'chase': [pygame.image.load(path).convert_alpha() for path in sprite_paths[self.variant]['chase']]
        }

        self.image = self.sprites['chase'][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        
    def move(self):
        # Волнообразное движение
        self.wave_offset += 0.05
        self.rect.x = self.rect.x + math.sin(self.wave_offset) * 2
        
        # Если игрок близко, начинаем преследование
        if self.distance_to_player() < self.chase_distance:
            self.current_animation = 'chase'
            self.chase_player()

        else:
            self.current_animation = 'swim'
            self.swim_pattern()
            
    def chase_player(self):
        # Логика преследования игрока
        player_pos = self.get_player_position()
        dx = player_pos[0] - self.rect.x
        dy = player_pos[1] - self.rect.y
        
        # Нормализуем вектор движения
        length = math.sqrt(dx**2 + dy**2)

        if length != 0:
            self.velocity_x = (dx/length) * self.swim_speed
            self.velocity_y = (dy/length) * self.swim_speed

    def swim_pattern(self):
        """Обычное плавание, когда игрок далеко"""
        self.velocity_y = math.sin(self.wave_offset) * 2
        self.velocity_x = math.cos(self.wave_offset) * 2