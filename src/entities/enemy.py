import math
import pygame
from src.config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, variant='default'):
        super().__init__()
        self.variant = variant
        self.x = x
        self.y = y
        
        # Физические параметры
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = -1  # -1 влево, 1 вправо
        self.on_ground = False
        
        # Параметры анимации
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.current_animation = 'idle'
        
        # Параметры врага
        self.health = 1
        self.is_alive = True
        self.can_be_stomped = True
        self.damage = 1


    def load_sprites(self):
        """
        Абстрактный метод, который должен быть переопределен в дочерних классах.
        Должен установить:
        - self.sprites (словарь с анимациями)
        - self.image (текущий спрайт)
        - self.rect (прямоугольник спрайта)
        """
        raise NotImplementedError("Subclass must implement load_sprites()")
        

    def load_sprites(self):
        self.sprites = {
            'idle': [],
            'walk': [],
            'death': []
        }
        
    def update(self):
        if self.is_alive:
            self.apply_gravity()
            self.move()
            self.animate()
            self.check_collisions()
        
    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += GRAVITY
            if self.velocity_y > MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED
        
    def move(self):
        self.rect.x += self.velocity_x * self.direction
        self.rect.y += self.velocity_y
        
    def animate(self):
        if not self.sprites[self.current_animation]:
            return
            
        self.animation_frame = (self.animation_frame + self.animation_speed) % len(self.sprites[self.current_animation])
        self.image = self.sprites[self.current_animation][int(self.animation_frame)]
        
        if self.direction > 0:  # Отражаем спрайт если движемся вправо
            self.image = pygame.transform.flip(self.image, True, False)
        
    def check_collisions(self):
        # Проверка коллизий с блоками
        pass

    def get_player_position(self):
        """Получает позицию игрока из текущей сцены"""
        if self.game and self.game.current_scene and self.game.current_scene.player:
            return (self.game.current_scene.player.rect.centerx, self.game.current_scene.player.rect.centery)
        
        return None
    
    def distance_to_player(self):
        """Вычисляет расстояние до игрока"""
        player_pos = self.get_player_position()

        if player_pos:
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery

            return math.sqrt(dx**2 + dy**2)
        
        return float('inf')
        
    def reverse_direction(self):
        self.direction *= -1
        
    def take_damage(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.die()
            
    def die(self):
        self.is_alive = False
        self.current_animation = 'death'
        self.animation_frame = 0
        # После окончания анимации смерти
        self.kill()