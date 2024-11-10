import pygame


class FireFlower(pygame.sprite.Sprite):
    def __init__(self, x, y, player, game, variant='dark'):
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
                'item_name': 'fireflower_blue',
                'image_path': 'assets/images/items/powerups/flower_yellow.png',
                'color': 'yellow'
            },
            {
                'item_name': 'fireflower_green',
                'image_path': 'assets/images/items/powerups/flower_green.png',
                'color': 'green'
            },
            {
                'item_name': 'fireflower_red',
                'image_path': 'assets/images/items/powerups/flower_red.png',
                'color': 'red'
            },
            {
                'item_name': 'fireflower_dark',
                'image_path': 'assets/images/items/powerups/flower_dark.png',
                'color': 'dark'
            }
        ]
    

    def load_sprites(self):       
        self.sprites = {
            'yellow': [
                pygame.image.load('assets/images/items/powerups/flower_yellow.png')
            ],
            'green': [
                pygame.image.load('assets/images/items/powerups/flower_green.png')
            ],
            'red': [
                pygame.image.load('assets/images/items/powerups/flower_red.png')
            ],
            'dark': [
                pygame.image.load('assets/images/items/powerups/flower_dark.png')
            ]
        }

        self.image = self.sprites[self.variant][0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    
    def update(self):
        if self.emerging:
             self.emerge()
        else:
            self.check_player_collision()


    def emerge(self):
        if self.rect.y > self.initial_y - self.emerge_height:
            self.rect.y -= 1
        else:
            self.emerging = False

    def check_player_collision(self):
        if pygame.sprite.collide_rect(self, self.player):

            self.game.sound_manager.play_sound('powerup')
            self.kill()
            self.invulnerability()

    def invulnerability(self):
        pass