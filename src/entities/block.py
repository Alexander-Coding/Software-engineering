import pygame
from src.config import *


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type, image_path, player, game):
        super().__init__()
        self.game = game
        self.player = player
        self.block_type = block_type
        self.image_path = image_path
        self.image = self.load_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.is_broken = 'brick' in str(self.image_path)
        
    def load_sprite(self):
        return pygame.image.load(str(self.image_path))
    
    def update(self):
        pass

    def break_block(self):
        if self.is_broken and self.player.is_big:
            self.game.game_state.score += 10
            self.game.sound_manager.play_sound('powerup')
            self.kill()