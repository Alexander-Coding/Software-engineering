import pygame
import pygame.locals
from src.config import *
from src.entities import powerups
from src.utils.animation import AnimationController


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, scene, variant, powerup_type='Mushroom'):
        super().__init__()
        self.scene = scene
        self.variant = variant
        self.powerup_type = powerup_type
        self.animation_controller = AnimationController()

        self.image = self.load_brick_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.load_brick_sprite()
        self.block_hit()

    
    def load_brick_sprite(self):
        return pygame.image.load('assets/images/blocks/bricks/brick.png')
    

    def block_hit(self):
        self.scene.game.sound_manager.play_sound('block_hit')
        powerup_obj = getattr(powerups, self.powerup_type)
        self.scene.all_sprites.add(powerup_obj(self.rect.x, self.rect.y, self.scene.player, self.scene.game, self.variant))


    def update(self):
        pass
