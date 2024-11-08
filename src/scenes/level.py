
import pygame
import json

from src.config import *
from src.entities.player import Player
from src.entities.block import Block
from src.entities import enemies

class Level:
    def __init__(self, game, level_id, level_data):
        super().__init__()  # Если наследуется от базового класса Scene
        self.game = game
        self.level_id = level_id
        self.camera_x = 0
        self.level_data = level_data
        # Инициализация групп спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = None
        
        # Загрузка уровня
        print(f"Загрузка уровня {level_id}")  # Отладка
        self.load_level()
        
        # Проверка загрузки
        if not self.player:
            print("Ошибка: игрок не создан!")
            self.player = Player(100, 100)  # Создаем игрока в дефолтной позиции
            self.all_sprites.add(self.player)

    def load_level(self):
        try:
            with open(f'levels\level_{self.level_id}.json', 'r') as f:
                level_data = json.load(f)
                print(f"Данные уровня загружены: {level_data}")
                
            for obj in level_data:
                try:
                    if obj['type'] == 'spawn':
                        print(f"Создание игрока на позиции {obj['x']}, {obj['y']}")
                        self.player = Player(obj['x'], obj['y'])
                        if not self.player:
                            raise Exception("Не удалось создать игрока")
                        
                        print("Игрок создан успешно")
                        self.all_sprites.add(self.player)
                        print("Игрок добавлен в группу спрайтов")

                        block = Block(obj['x'], obj['y'], obj['asset_name'], obj['image_path'])
                        self.all_sprites.add(block)
                        
                    elif obj['type'] == 'block':
                        print(f"Создание блока на позиции {obj['x']}, {obj['y']}")
                        block = Block(obj['x'], obj['y'], obj['asset_name'], obj['image_path'])
                        self.blocks.add(block)
                        self.all_sprites.add(block)
                        print("Блок создан и добавлен")

                    elif obj['type'] == 'enemy':
                        enemy = getattr(enemies, obj['class'])

                        if obj['behavior'] == None:
                            enemy_obj = enemy(obj['x'], obj['y'], obj['color'])

                        else:
                            enemy_obj = enemy(obj['x'], obj['y'], obj['color'], obj['behavior'])

                        enemy_obj.game = self.game  # Устанавливаем ссылку на игру
                        self.enemies.add(enemy_obj)
                        self.all_sprites.add(enemy_obj)

                    else:
                        block = Block(obj['x'], obj['y'], obj['asset_name'], obj['image_path'])
                        self.all_sprites.add(block)
                        
                except Exception as e:
                    print(f"Ошибка при создании объекта {obj}: {e}")
                    continue
            self.player.blocks = self.blocks
            print(f"Всего спрайтов: {len(self.all_sprites)}")
            print(f"Всего блоков: {len(self.blocks)}")
            print(f"Игрок существует: {self.player is not None}")
                    
        except Exception as e:
            print(f"Ошибка загрузки уровня: {e}")
            self.create_default_level()

    def create_default_level(self):
        print("Создание тестового уровня")
        # Создаем игрока
        self.player = Player(100, 100)
        self.all_sprites.add(self.player)
        
        # Создаем платформу
        for x in range(0, 800, 32):
            block = Block(x, 500)
            self.blocks.add(block)
            self.all_sprites.add(block)

    def update(self):
        try:
            if not self.player or len(self.all_sprites) == 0:
                print("Ошибка: уровень не инициализирован корректно")
                self.create_default_level()
                return
                
            # Обновляем всех спрайтов
            self.all_sprites.update()

            # Обновляем игрока
            if self.player:
                self.player.update()

            # Обновляем позицию камеры
            self.update_camera()
                
        except Exception as e:
            print(f"Ошибка при обновлении уровня: {e}")
            import traceback
            traceback.print_exc()

    def update_camera(self):
        try:
            if self.player:
                target_x = self.player.rect.centerx - WINDOW_WIDTH // 2
                self.camera_x += (target_x - self.camera_x) * 0.1
        except Exception as e:
            print(f"Ошибка при обновлении камеры: {e}")

    def draw(self, screen):
        try:
            screen.fill((107, 140, 255))  # Цвет неба
            
            # Отрисовка всех спрайтов с учетом позиции камеры
            for sprite in self.all_sprites:
                screen.blit(sprite.image, 
                           (sprite.rect.x - int(self.camera_x), sprite.rect.y))
                           
            pygame.display.flip()
            
        except Exception as e:
            print(f"Ошибка при отрисовке уровня: {e}")

    def handle_event(self, event):
        print(f"Обработка события в уровне: {event}")  # Отладка
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from src.scenes.menu import MainMenu
                self.game.change_scene(MainMenu(self.game))
            elif self.player:
                self.player.handle_movement()
                
    def pause_game(self):
        self.game.is_paused = True
        # Показать меню паузы

    def handle_collisions(self):
        # Коллизии с врагами
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            if self.player.velocity_y > 0:
                enemy.kill()
                self.player.velocity_y = -10
            else:
                self.player_hit()
                
    def player_hit(self):
        if not self.player.is_invincible:
            if self.player.is_big:
                self.player.is_big = False
            else:
                self.game_over()
                
    def game_over(self):
        # Показать экран game over
        pass
