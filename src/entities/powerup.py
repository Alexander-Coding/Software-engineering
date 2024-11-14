import pygame
import pygame.locals
from src.config import *
from resource_path import resource_path
from src.entities import powerups


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, scene, variant, powerup_type='Mushroom'):
        super().__init__()
        self.scene = scene
        self.variant = variant
        self.powerup_type = powerup_type

        self.is_broken = False
        self.is_active = True

        self.image = self.load_brick_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.load_brick_sprite()

    
    def load_brick_sprite(self):
        return pygame.image.load(resource_path('assets/images/blocks/bricks/brick.png'))
    

    def block_hit(self):
        #self.scene.game.sound_manager.play_sound('block_hit')
        powerup_obj = getattr(powerups, self.powerup_type)
        self.scene.all_sprites.add(powerup_obj(self.rect.x, self.rect.y, self.scene.player, self.scene.game, self.variant))


    def update(self):
        pass

    def break_block(self):
        if self.is_active:
            self.is_active = False
            self.block_hit()
            return

        if not self.is_active and self.scene.player.is_big:
            self.scene.game.game_state.score += 10
            self.scene.game.sound_manager.play_sound('powerup')
            self.kill()