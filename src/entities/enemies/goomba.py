import pygame
from src.entities.enemy import Enemy


class Goomba(Enemy):
    def __init__(self, x, y, variant='dark'):
        super().__init__(x, y, variant)
        self.velocity_x = 2
        self.animation_speed = 0.15
        self.enemy_name = f'goomba_{variant}'

        self.load_sprites()


    @classmethod
    def get_variants(cls):
        return [
            {
                'enemy_name': 'goomba_dark',
                'image_path': 'assets/images/enemies/goombas/goomba_dark/walk1.png',
                'color': 'dark',
                'behavior': None
            }
        ]
        

    def load_sprites(self):
        sprite_paths = {
            'dark': {
                'idle': [
                    'assets/images/enemies/goombas/goomba_dark/walk1.png', 
                    'assets/images/enemies/goombas/goomba_dark/walk2.png'
                    ],
                'death': [
                    'assets/images/enemies/goombas/goomba_dark/squashed.png'
                    ]
            }
        }
        
        self.sprites = {
            'idle': [pygame.image.load(path).convert_alpha() for path in sprite_paths[self.variant]['idle']],
            'death': [pygame.image.load(path).convert_alpha() for path in sprite_paths[self.variant]['death']]
        }

        self.image = self.sprites['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

    def move(self):
        super().move()