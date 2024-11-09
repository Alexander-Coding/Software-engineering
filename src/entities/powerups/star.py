import pygame


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, player, game, variant='dark'):
        super().__init__()
        self.x = x
        self.y = y
        self.player = player
        self.game = game
        self.variant = variant
        self.load_sprites()


    @classmethod
    def get_variants(cls):
        return [
            {
                'item_name': 'star_dark',
                'image_path': 'assets/images/items/powerups/star_dark.png',
                'color': 'dark'
            },
            {
                'item_name': 'star_green',
                'image_path': 'assets/images/items/powerups/star_green.png',
                'color': 'green'
            },
            {
                'item_name': 'star_red',
                'image_path': 'assets/images/items/powerups/star_red.png',
                'color': 'red'
            },
            {
                'item_name': 'star_white',
                'image_path': 'assets/images/items/powerups/star_white.png',
                'color': 'white'
            }
        ]
    

    def load_sprites(self):       
        self.sprites = {
            'dark': [
                pygame.image.load('assets/images/items/powerups/star_dark.png')
            ],
            'green': [
                pygame.image.load('assets/images/items/powerups/star_green.png')
            ],
            'red': [
                pygame.image.load('assets/images/items/powerups/star_red.png')
            ],
            'white': [
                pygame.image.load('assets/images/items/powerups/star_white.png')
            ]
        }

        self.image = self.sprites[self.variant][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y - 32