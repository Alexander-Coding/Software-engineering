import pygame
from src.config import *
from src.utils.animation import AnimationController

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type='mushroom'):
        super().__init__()
        self.powerup_type = powerup_type
        self.animation_controller = AnimationController()
        self.load_sprites()
        
        self.image = self.sprites[self.powerup_type][0]
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
        
    def load_sprites(self):
        self.sprites = {
            'mushroom': [],  # Спрайты гриба
            'flower': [],    # Спрайты цветка
            'star': [],      # Спрайты звезды
            '1up': []        # Спрайты доп. жизни
        }
        
        # Загрузка анимаций для разных типов бонусов
        for powerup_type in self.sprites:
            if powerup_type == 'star':
                self.animation_controller.add_animation(
                    powerup_type,
                    self.sprites[powerup_type],
                    frame_duration=0.1,
                    loop=True
                )
                
    def update(self):
        if self.emerging:
            self.emerge()
        else:
            self.move()
            self.apply_gravity()
            self.animate()
            
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

class Mushroom(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, 'mushroom')

class FireFlower(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, 'flower')
        
    def update(self):
        if self.emerging:
            self.emerge()
        else:
            self.animate()
            # Цветок не двигается после появления

class Star(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, 'star')
        self.bounce_power = -8
        
    def update(self):
        if self.emerging:
            self.emerge()
        else:
            self.move()
            self.apply_gravity()
            self.animate()
            
            # Звезда отскакивает при приземлении
            if self.velocity_y > 0:  # Падение
                self.check_bounce()
                
    def check_bounce(self):
        # Проверка столкновения с блоками
        if pygame.sprite.spritecollide(self, self.game.blocks, False):
            self.velocity_y = self.bounce_power

class OneUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, '1up')
