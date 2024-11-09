import pygame
import pygame.locals
import time
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
        
        # Физические параметры
        self.velocity_x = 2
        self.velocity_y = 0
        self.active = False
        
        # Анимация появления
        self.emerging = True
        self.emerge_height = 32
        self.initial_y = y

        self.load_brick_sprite()
        self.block_hit()

    
    def load_brick_sprite(self):
        return pygame.image.load('assets/images/blocks/bricks/brick.png')
    

    def block_hit(self):
        powerup_obj = getattr(powerups, self.powerup_type)
        self.scene.all_sprites.add(powerup_obj(self.rect.x, self.rect.y, self.scene.player, self.scene.game, self.variant))


    def update(self):
        # if self.emerging:
        #     self.emerge()
        # else:
        #     self.move()
        #     self.apply_gravity()
        #     self.animate()
        pass
            
    def emerge(self):
        if self.rect.y > self.initial_y - self.emerge_height:
            self.rect.y -= 1
        else:
            self.emerging = False
            self.active = True
            
    def move(self):
        if self.active:
            self.rect.x += self.velocity_x
            
    def apply_gravity(self):
        if self.active and self.powerup_type != 'flower':  # Цветок не падает
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y
            
    def animate(self):
        if self.powerup_type == 'star':
            self.image = self.animation_controller.update(0.1)
            
    def reverse_direction(self):
        self.velocity_x *= -1
        
    def collect(self, player):
        """Применяет эффект бонуса к игроку"""
        if self.powerup_type == 'mushroom':
            if not player.is_big:
                player.grow()
        elif self.powerup_type == 'flower':
            player.get_fire_power()
        elif self.powerup_type == 'star':
            player.make_invincible()
        elif self.powerup_type == '1up':
            player.add_life()
            
        # Воспроизведение звука
        from utils.sound_manager import SoundManager
        SoundManager().play_sound('powerup')
        
        # Начисление очков
        from utils.scoring import ScoringSystem
        ScoringSystem(player.game.game_state).add_score('powerup')
        
        # Удаление бонуса
        self.kill()
