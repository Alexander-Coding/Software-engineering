import pygame


class Mashroom(pygame.sprite.Sprite):
    def __init__(self, x, y, player, game, variant='red'):
        super().__init__()
        self.x = x
        self.y = y
        self.player = player
        self.game = game
        self.variant = variant
        self.load_sprites()

        # Анимация появления
        self.emerging = True
        self.emerge_height = 32
        self.initial_y = y


    @classmethod
    def get_variants(cls):
        return [
            {
                'item_name': 'mashroom_blue',
                'image_path': 'assets/images/items/powerups/mashroom_blue.png',
                'color': 'blue'
            },
            {
                'item_name': 'mashroom_green',
                'image_path': 'assets/images/items/powerups/mashroom_green.png',
                'color': 'green'
            },
            {
                'item_name': 'mashroom_red',
                'image_path': 'assets/images/items/powerups/mashroom_red.png',
                'color': 'red'
            }
        ]
    

    def load_sprites(self):       
        self.sprites = {
            'blue': [
                pygame.image.load('assets/images/items/powerups/mashroom_blue.png')
            ],
            'green': [
                pygame.image.load('assets/images/items/powerups/mashroom_green.png')
            ],
            'red': [
                pygame.image.load('assets/images/items/powerups/mashroom_red.png')
            ]
        }

        self.image = self.sprites[self.variant][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    
    def update(self):
        if self.emerging:
             self.emerge()


    def emerge(self):
        if self.rect.y > self.initial_y - self.emerge_height:
            self.rect.y -= 1
        else:
            self.emerging = False
            self.active = True