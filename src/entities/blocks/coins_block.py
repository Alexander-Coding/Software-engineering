import pygame
import random
from src.entities import Coin


class FlyCoins(Coin):
    def __init__(self, x, y, player, game):
        super().__init__(x, y, player, game)
        self.start_rect_y = y
    
    def update(self):
        super().animate()

        if self.rect.y > self.start_rect_y - 32:
            self.rect.y -= 1

        else:
            self.kill()


class CoinsBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, player, game):
        super().__init__()
        self.game = game
        self.player = player
        self.image = self.load_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.coin_count = self.get_coin_count()
        self.empty_block_asset = self.get_empty_block_asset()

    @staticmethod
    def get_asset():
        return pygame.image.load('assets/images/blocks/question/question.png')

    def load_sprite(self):
        return pygame.image.load('assets/images/blocks/question/question.png')

    def get_empty_block_asset(self):
        return pygame.image.load('assets/images/blocks/question/empty.png')

    def get_coin_count(self):
        return random.randint(3, 15)
    
    def break_block(self):
        if self.coin_count > 0:
            self.game.game_state.score += 10
            self.game.game_state.coins += 1
            self.game.sound_manager.play_sound('coins')
            self.coin_count -= 1
            self.game.current_scene.all_sprites.add(FlyCoins(self.rect.centerx, self.rect.top - 32, self.player, self.game))
        else:
            self.image = self.empty_block_asset

