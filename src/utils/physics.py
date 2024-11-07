import pygame
import sys
sys.path.append(r'C:\Users\Alexa\github\BioSense\mario\src')
from config import *

class PhysicsEngine:
    @staticmethod
    def check_collision(sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False)
    
    @staticmethod
    def resolve_collision(entity, blocks):
        hits = pygame.sprite.spritecollide(entity, blocks, False)
        
        for block in hits:
            # Вертикальные коллизии
            if entity.velocity_y > 0:  # Падение
                entity.rect.bottom = block.rect.top
                entity.velocity_y = 0
                entity.on_ground = True
            elif entity.velocity_y < 0:  # Прыжок
                entity.rect.top = block.rect.bottom
                entity.velocity_y = 0
                
            # Горизонтальные коллизии
            if entity.velocity_x > 0:  # Движение вправо
                entity.rect.right = block.rect.left
            elif entity.velocity_x < 0:  # Движение влево
                entity.rect.left = block.rect.right
                
    @staticmethod
    def apply_gravity(entity):
        if not entity.on_ground:
            entity.velocity_y += GRAVITY
            if entity.velocity_y > 20:  # Максимальная скорость падения
                entity.velocity_y = 20
                
    @staticmethod
    def check_platform_edges(entity, blocks):
        # Проверка краёв платформы для врагов
        entity.rect.x += 2
        right_check = pygame.sprite.spritecollide(entity, blocks, False)
        entity.rect.x -= 4
        left_check = pygame.sprite.spritecollide(entity, blocks, False)
        entity.rect.x += 2
        
        if not right_check and entity.velocity_x > 0:
            entity.reverse_direction()
        elif not left_check and entity.velocity_x < 0:
            entity.reverse_direction()