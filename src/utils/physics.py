import pygame
from src.config import *

class PhysicsEngine:
    @staticmethod
    def check_collision(sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False)
    
    @staticmethod
    def resolve_collision(entity, blocks):
        original_rect = self.rect.copy()

        # Проверяем вертикальные коллизии
        self.rect.y += self.velocity_y  # Сначала обновляем вертикальную позицию
        blocks_hit = pygame.sprite.spritecollide(self, self.blocks, False)

        for block in blocks_hit:
            if self.velocity_y > 0:  # Падение вниз
                print("НИЗ")
                self.rect.bottom = block.rect.top  # Устанавливаем нижнюю границу игрока на верхнюю границу блока
                self.velocity_y = 0  # Обнуляем вертикальную скорость
                self.on_ground = True  # Игрок теперь на земле
            elif self.velocity_y < 0:  # Подъем вверх
                print("ВВЕРХ")
                self.rect.top = block.rect.bottom  # Устанавливаем верхнюю границу игрока на нижнюю границу блока
                self.velocity_y = 0  # Обнуляем вертикальную скорость

        # Проверяем горизонтальные коллизии
        current_rect = self.rect.copy()
        self.rect.x += self.velocity_x
        blocks_hit_horizontal = pygame.sprite.spritecollide(self, self.blocks, False)

        for block in blocks_hit_horizontal:
            if self.velocity_x > 0:  # Движение вправо
                print("ПРАВО")
                self.rect.right = block.rect.left
            elif self.velocity_x < 0:  # Движение влево
                print("ВЛЕВО")
                self.rect.left = block.rect.right

                # Проверка состояния on_ground после обработки коллизий
        if not blocks_hit:  # Если нет вертикальных коллизий
            self.on_ground = False

            # Проверка на наличие блока под игроком
            for block in self.blocks:
                if (self.rect.bottom >= block.rect.top and
                        self.rect.bottom <= block.rect.bottom and
                        self.rect.centerx >= block.rect.left and
                        self.rect.centerx <= block.rect.right):
                    print("Находимся на блоке")
                    self.on_ground = True
                    break
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