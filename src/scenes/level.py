import pygame

from src.config import *
from src.entities.player import Player
from src.entities.block import Block
from src.entities.blocks.finish_block import FinishBlock 
from src.entities.powerup import PowerUp
from src.entities.coin import Coin
from src.entities.blocks import CoinsBlock
from src.entities import enemies
from src.scenes.pause_menu import PauseMenu


class Level:
    def __init__(self, game, level_name, level_data):
        self.game = game
        self.level_name = level_name
        self.camera_x = 0
        self.level_data = level_data
        self.sound_manager = self.game.sound_manager
        # Инициализация групп спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = None

        self.heart_asset = self.load_heart_asset()
        self.coin_asset = self.load_coin_asset()
        
        # Загрузка уровня
        print(f"Загрузка уровня {level_name}")  # Отладка
        self.load_level()
        
        # Проверка загрузки
        if not self.player:
            print("Ошибка: игрок не создан!")
            self.player = Player(100, 100)  # Создаем игрока в дефолтной позиции
            self.all_sprites.add(self.player)

    def load_heart_asset(self):
        return pygame.transform.scale(pygame.image.load('assets/images/ui/heart.png').convert_alpha(), (16, 16))
    
    def load_coin_asset(self):
        return pygame.transform.scale(pygame.image.load('assets/images/ui/coin.png').convert_alpha(), (16, 16))

    def load_level(self):
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = None
        self.camera_x = 0

        for obj in self.level_data:
            if obj['type'] == 'spawn':
                self.player = Player(obj['x'], obj['y'], self.game)
                block = Block(obj['x'], obj['y'], obj['type'], obj['image_path'], self.player, self.game)
                
                self.all_sprites.add(block)


        for obj in self.level_data:
            if obj['type'] == 'block':
                block = Block(obj['x'], obj['y'], obj['type'], obj['image_path'], self.player, self.game)

                self.blocks.add(block)
                self.all_sprites.add(block)

            elif obj['type'] == 'enviroment':
                block = Block(obj['x'], obj['y'], obj['type'], obj['image_path'], self.player, self.game)
                self.all_sprites.add(block)

            elif obj['type'] == 'powerup':
                powerup = PowerUp(obj['x'], obj['y'], self, obj['color'], obj['class'])
                self.blocks.add(powerup)
                self.all_sprites.add(powerup)


        for obj in self.level_data:
            if obj['type'] == 'finish':
                block = FinishBlock(obj['x'], obj['y'], obj['type'], obj['image_path'], self.player, self.game, self.level_name)
                self.all_sprites.add(block)

            elif obj['type'] == 'coin':
                coin = Coin(obj['x'], obj['y'], self.player, self.game)
                self.all_sprites.add(coin)

            elif obj['type'] == 'question':
                question = CoinsBlock(obj['x'], obj['y'], self.player, self.game)
                self.blocks.add(question)
                self.all_sprites.add(question)

            elif obj['type'] == 'enemy':
                enemy = getattr(enemies, obj['class'])

                if obj['behavior'] == None:
                    enemy_obj = enemy(obj['x'], obj['y'], self.player, self.game, self.blocks, obj['color'])

                else:
                    enemy_obj = enemy(obj['x'], obj['y'], self.player, self.game, self.blocks, obj['color'], obj['behavior'])

                self.enemies.add(enemy_obj)
                self.all_sprites.add(enemy_obj)

        self.player.blocks = self.blocks
        

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
                # Получаем текущую позицию камеры
                current_camera_x = self.camera_x

                # Вычисляем целевую позицию по оси X
                target_x = self.player.rect.centerx - WINDOW_WIDTH // 2

                # Обновляем камеру только если игрок движется вправо
                if target_x > current_camera_x:
                    self.camera_x += (target_x - current_camera_x) * 0.1
                    self.player.leftside = self.camera_x
        except Exception as e:
            print(f"Ошибка при обновлении камеры: {e}")

    def draw(self, screen):
        try:
            screen.fill((107, 140, 255))  # Цвет неба
            
            # Отрисовка всех спрайтов с учетом позиции камеры
            for sprite in self.all_sprites:
                screen.blit(sprite.image, (sprite.rect.x - int(self.camera_x), sprite.rect.y - sprite.image.get_height()))

            font = pygame.font.Font(None, 36)  # Шрифт для названия уровня
            title_surface = font.render(self.level_name, True, (255, 255, 255))  # Белый цвет
            screen.blit(title_surface, (10, 10))  # Позиция в левом верхнем углу
            
            # Отрисовка счета
            score_surface = font.render(f"Очки: {self.game.game_state.score}", True, (255, 255, 255))
            screen.blit(score_surface, (WINDOW_WIDTH - 150, 10))  # Позиция справа сверху

            screen.blit(self.coin_asset, (WINDOW_WIDTH - 260, 14))
            score_surface = font.render(f": {self.game.game_state.coins}", True, (255, 255, 255))
            screen.blit(score_surface, (WINDOW_WIDTH - 240, 10))

            # Отрисовка жизней
            for i in range(self.game.game_state.live):
                screen.blit(self.heart_asset, (WINDOW_WIDTH - 300 - (i * (24)), 14))  # Позиция для сердечек

            # отрисовка игрока
            screen.blit(self.player.image, (self.player.rect.x - int(self.camera_x), self.player.rect.y - 32))

            pygame.display.flip()
            
        except Exception as e:
            print(f"Ошибка при отрисовке уровня: {e}")

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               self.pause_game()
            elif self.player:
                self.player.handle_movement()
                
    def pause_game(self):
        self.game.is_paused = True
        self.game.change_scene(PauseMenu(self.game, self))


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
        self.sound_manager.play_misic('death')
        # Показать экран game over
        pass
