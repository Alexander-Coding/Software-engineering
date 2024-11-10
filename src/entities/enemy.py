import math
import pygame
from src.config import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, variant='default'):
        super().__init__()

        self.player = None
        self.blocks = None

        self.variant = variant
        self.x = x
        self.y = y

        self.reverse_interval = 500
        self.attack_time = pygame.time.get_ticks()
        self.last_reverse_time = pygame.time.get_ticks()

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
        """Абстрактный метод для загрузки спрайтов"""
        raise NotImplementedError("Subclass must implement load_sprites()")

    def update(self):
        if self.is_alive:
            self.apply_gravity()
            self.animate()
        else:
            self.die()

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += GRAVITY
            if self.velocity_y > MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED

    def animate(self):
        if not self.sprites[self.current_animation]:
            return

        # Обновляем анимацию
        self.animation_frame = (self.animation_frame + self.animation_speed) % len(self.sprites[self.current_animation])
        self.image = self.sprites[self.current_animation][int(self.animation_frame)]

        if self.direction > 0:  # Отражаем спрайт если движемся вправо
            self.image = pygame.transform.flip(self.image, True, False)

    def check_collisions(self):
        blocks_hit = pygame.sprite.spritecollide(self, self.blocks, False)

        for block in blocks_hit:
            if self.velocity_x > 0:
                self.rect.right = block.rect.left
                self.reverse_direction()

            elif self.velocity_x < 0:
                self.rect.left = block.rect.right
                self.reverse_direction()

    def distance_to_player(self):
        """Calculates the distance to the player."""
        player_pos = self.get_player_position()
        if player_pos:
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            return math.sqrt(dx ** 2 + dy ** 2)
        return float('inf')

    def get_player_position(self):
        """Gets the player's position from the current scene."""
        if self.game and self.game.current_scene and self.game.current_scene.player:
            return (self.game.current_scene.player.rect.centerx, self.game.current_scene.player.rect.centery)
        return None

    def reverse_direction(self):
        """Изменяем направление движения"""
        self.direction *= -1

    def Attack(self):
        if self.rect.colliderect(self.player.rect.move(-1, 0)) or self.rect.colliderect(self.player.rect.move(1, 0)):  # Проверяем, есть ли коллизия с блоком чуть ниже персонажа
            return True
        return False

    def die(self):
        """Умираем"""
        self.is_alive = False
        self.kill()
        # Устанавливаем анимацию смерти и удаляем объект после завершения анимации