import pygame
from src.config import *
from resource_path import resource_path


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, player, game):
        super().__init__()
        self.load_sprites()
        self.image = self.sprites[1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.game = game
        self.animation_frame = 0


    @staticmethod
    def get_image():
        return pygame.image.load(resource_path('assets/images/items/coin/coin_spin_2.png'))
    

    @staticmethod
    def get_image_path():
        return 'assets/images/items/coin/coin_spin_2.png'
        

    def load_sprites(self):
        self.sprites = [
            pygame.image.load(resource_path('assets/images/items/coin/coin_spin_1.png')),
            pygame.image.load(resource_path('assets/images/items/coin/coin_spin_2.png')),
            pygame.image.load(resource_path('assets/images/items/coin/coin_spin_3.png'))
        ]
        
    def update(self):
        self.animate()
        self.check_player_collision()
        
    def animate(self):
        self.animation_frame = (self.animation_frame + 0.1) % len(self.sprites)
        self.image = self.sprites[int(self.animation_frame)]

    def check_player_collision(self):
        if pygame.sprite.collide_rect(self, self.player):
            self.game.game_state.coins += 1
            self.game.game_state.score += 10
            self.game.sound_manager.play_sound('coins')
            self.kill()
    