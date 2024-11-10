import pygame
from src.entities.block import Block


class FinishBlock(Block):
    def __init__(self, x, y, block_type, image_path, player, game, level):
        super().__init__(x, y, block_type, image_path, player, game)
        self.game = game
        self.level = level

    def update(self):
        self.check_player_collision()

    def check_player_collision(self):
        if pygame.sprite.collide_rect(self, self.player):
            self.game.game_state.score += 1000
            self.game.sound_manager.play_sound('powerup')
            self.game.game_state.complete_level(self.level)
            self.game.level_complete()
            self.kill()
