import pygame
import json
import os

from pathlib import Path
from src.config import *
from src.scenes.menu import MainMenu
from src.entities.enemies import get_all_enemies
from src.entities.powerups import get_all_powerups
from src.entities.coin import Coin
from pygame.locals import *


class LevelEditor:
    def __init__(self, game, level_name, level_data):
        self.game = game
        self.grid_size = 32
        self.current_tile = None
        self.tiles = {}
        self.level_name = level_name
        self.level_data = level_data
        self.camera_x = 0
        self.asset_list_rect = pygame.Rect(WINDOW_WIDTH - 200, 0, 200, WINDOW_HEIGHT)
        self.asset_buttons = []
        self.scroll_y = 0
        self.mouse_held = False
        self.load_block_assets()
        self.load_enemies()
        self.load_powerups()
        
        # Кнопка сохранения уровня
        self.save_button_rect = pygame.Rect(10, WINDOW_HEIGHT - 50, 100, 40)
        
        # Параметры диалогового окна
        self.showing_save_dialog = False
        self.dialog_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 75, 300, 150)
        self.input_rect = pygame.Rect(self.dialog_rect.x + 20, self.dialog_rect.y + 60, 260, 30)


    def load_block_assets(self):
        assets_path = Path('assets/images/blocks')

        for asset_file in assets_path.rglob('*.png'):
            asset_name = asset_file.stem
            image = pygame.image.load(str(asset_file))
            
            self.tiles[asset_name] = image
            button_rect = pygame.Rect(WINDOW_WIDTH - 180, len(self.asset_buttons) * 40 + 10, 160, 32)

            if asset_name == 'big_castle':
                self.asset_buttons.append({'rect': button_rect, 'name': asset_name,  'type': 'finish', 'image_path': str(asset_file)})

            elif asset_name == 'small_castle':
                self.asset_buttons.append({'rect': button_rect, 'name': asset_name,  'type': 'spawn', 'image_path': str(asset_file)})

            elif asset_name == 'question':
                self.asset_buttons.append({'rect': button_rect, 'name': asset_name,  'type': 'question', 'image_path': str(asset_file)})

            else:
                if "enviroment" in str(asset_file) or "colors" in str(asset_file):
                    self.asset_buttons.append({'rect': button_rect, 'name': asset_name,  'type': 'enviroment', 'image_path': str(asset_file)})

                elif "flags" in str(asset_file):
                    self.asset_buttons.append({'rect': button_rect, 'name': asset_name,  'type': 'flag', 'image_path': str(asset_file)})

                else:
                    self.asset_buttons.append({'rect': button_rect, 'name': asset_name,  'type': 'block', 'image_path': str(asset_file)})


    def load_enemies(self):
        enemies = get_all_enemies()

        for enemy in enemies:
            asset_name = enemy['enemy_name']
            image = pygame.image.load(str(enemy['image_path']))

            aspect_ratio = image.get_width() / image.get_height()

            if aspect_ratio > 1:
                new_width = self.grid_size
                new_height = int(self.grid_size / aspect_ratio)

            else:
                new_width = int(self.grid_size * aspect_ratio)
                new_height = self.grid_size

            self.tiles[asset_name] = pygame.transform.scale(image, (new_width, new_height))
            button_rect = pygame.Rect(WINDOW_WIDTH - 180, len(self.asset_buttons) * 40 + 10, 160, 32)

            self.asset_buttons.append({
                'rect': button_rect, 
                'name': asset_name,  
                'type': 'enemy', 
                'class': enemy['class'], 
                'color': enemy['color'], 
                'image_path': enemy['image_path'], 
                'behavior': enemy['behavior']
            })

        
    def load_powerups(self):
        self.tiles['coin'] = Coin.get_image()
        button_rect = pygame.Rect(WINDOW_WIDTH - 180, len(self.asset_buttons) * 40 + 10, 160, 32)

        self.asset_buttons.append({
            'rect': button_rect, 
            'name': 'coin',  
            'type': 'coin', 
            'class': 'Coin', 
            'image_path': Coin.get_image_path(), 
        })


        powerups = get_all_powerups()

        for powerup in powerups:
            asset_name = powerup['item_name']
            image = pygame.image.load(str(powerup['image_path']))

            aspect_ratio = image.get_width() / image.get_height()

            if aspect_ratio > 1:
                new_width = self.grid_size
                new_height = int(self.grid_size / aspect_ratio)

            else:
                new_width = int(self.grid_size * aspect_ratio)
                new_height = self.grid_size

            self.tiles[asset_name] = pygame.transform.scale(image, (new_width, new_height))
            button_rect = pygame.Rect(WINDOW_WIDTH - 180, len(self.asset_buttons) * 40 + 10, 160, 32)

            self.asset_buttons.append({
                'rect': button_rect, 
                'name': asset_name,  
                'type': 'powerup', 
                'class': powerup['class'], 
                'color': powerup['color'], 
                'image_path': powerup['image_path'], 
            })


    def handle_event(self, event):
        if self.showing_save_dialog:
            # Обработка событий в диалоговом окне
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.level_name = self.level_name[:-1]

                elif event.key == pygame.K_RETURN:
                    self.save_level(self.level_name)
                    self.showing_save_dialog = False
                    self.level_name = ""

                else:
                    self.level_name += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка нажатия на область диалога для закрытия
                if not self.dialog_rect.collidepoint(event.pos):
                    self.showing_save_dialog = False
                    self.level_name = ""
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                grid_x = (mouse_pos[0] + self.camera_x) // self.grid_size
                grid_y = (mouse_pos[1] // self.grid_size) + 1
                
                if event.button == 3:  # ПКМ
                    # Проверка на наличие ассета по координатам и его удаление
                    self.level_data = [tile for tile in self.level_data if not (tile['x'] == grid_x * self.grid_size and tile['y'] == grid_y * self.grid_size)]
                
                elif event.button == 1:  # ЛКМ
                    if self.save_button_rect.collidepoint(mouse_pos):
                        self.mouse_held = False

                        if self.level_name == 'Новый уровень':
                            self.showing_save_dialog = True
                        else:
                            self.save_level(self.level_name)

                    elif self.asset_list_rect.collidepoint(mouse_pos):
                        adjusted_y = mouse_pos[1] + self.scroll_y

                        for button in self.asset_buttons:
                            if button['rect'].collidepoint(mouse_pos[0], adjusted_y):
                                self.current_tile = button
                                break
                            
                    else:
                        if self.current_tile:
                            self.mouse_held = True
                            self.place_tile()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse_held = False
            
            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_y = max(0, min(self.scroll_y - event.y * 20,
                                           max(0, len(self.asset_buttons) * 40 - WINDOW_HEIGHT)))
                
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_scene(MainMenu(self.game))


    def place_tile(self):
        mouse_pos = pygame.mouse.get_pos()
        grid_x = (mouse_pos[0] + self.camera_x) // self.grid_size
        grid_y = (mouse_pos[1] // self.grid_size) + 1

        if self.current_tile['type'] == 'enemy':
            tile_data = {
                'asset_name': self.current_tile['name'],
                'image_path': self.current_tile['image_path'],
                'type':       self.current_tile['type'],
                'class':      self.current_tile['class'],
                'color':      self.current_tile['color'],
                'behavior':   self.current_tile['behavior'],
                'x': grid_x * self.grid_size,
                'y': grid_y * self.grid_size
            }

        elif self.current_tile['type'] == 'powerup':
            tile_data = {
                'asset_name': self.current_tile['name'],
                'image_path': self.current_tile['image_path'],
                'type':       self.current_tile['type'],
                'class':      self.current_tile['class'],
                'color':      self.current_tile['color'],
                'x': grid_x * self.grid_size,
                'y': grid_y * self.grid_size
            }

        else:
            tile_data = {
                'asset_name': self.current_tile['name'],
                'image_path': self.current_tile['image_path'],
                'type':       self.current_tile['type'],
                'x': grid_x * self.grid_size,
                'y': grid_y * self.grid_size
            }

        if tile_data not in self.level_data:
            self.level_data.append(tile_data)
        

    def save_level(self, name):
        os.makedirs('levels', exist_ok=True)
        filename = f'levels/{name}.json'
        
        with open(filename, 'w') as f:
            json.dump(self.level_data, f)


    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.camera_x = max(0, self.camera_x - 5)

        if keys[pygame.K_RIGHT]:
            self.camera_x += 5

        if self.mouse_held and self.current_tile:
            self.place_tile()
            

    def draw(self, screen):
        screen.fill(WHITE)
        
        for x in range(0, WINDOW_WIDTH + self.grid_size, self.grid_size):
            pygame.draw.line(screen, (200, 200, 200), 
                           (x - self.camera_x % self.grid_size, 0), 
                           (x - self.camera_x % self.grid_size, WINDOW_HEIGHT))
            
        for y in range(0, WINDOW_HEIGHT + self.grid_size, self.grid_size):
            pygame.draw.line(screen, (200, 200, 200), 
                           (0, y), 
                           (WINDOW_WIDTH, y))
            
        for tile in self.level_data:
            tile_image = self.tiles[tile['asset_name']]
            screen.blit(tile_image, (tile['x'] - self.camera_x, tile['y'] - tile_image.get_height()))
            
        pygame.draw.rect(screen, (200, 200, 200), self.asset_list_rect)
        
        for button in self.asset_buttons:
            button_rect = button['rect'].copy()
            button_rect.y -= self.scroll_y

            if self.asset_list_rect.contains(button_rect):
                if self.current_tile and button['name'] == self.current_tile['name']:
                    color = (100, 100, 250)  # Синий цвет для выделенной кнопки
                else:
                    color = (150, 150, 150)  # Обычный цвет для кнопок

                pygame.draw.rect(screen, color, button_rect)
                image = pygame.transform.scale(self.tiles[button['name']], (32, 32))
                screen.blit(image, (button_rect.x + 5, button_rect.y + 2))
                font = pygame.font.Font(None, 20)
                text = font.render(button['name'], True, (0, 0, 0))
                screen.blit(text, (button_rect.x + 40, button_rect.y + 8))
        
        # Рисуем кнопку сохранения
        pygame.draw.rect(screen, (0, 255, 0), self.save_button_rect)
        font = pygame.font.Font(None, 24)
        save_text = font.render("Сохранить", True, (0, 0, 0))
        screen.blit(save_text, (self.save_button_rect.x + 10, self.save_button_rect.y + 10))
        
        # Рисуем диалоговое окно, если оно активно
        if self.showing_save_dialog:
            self.draw_save_dialog(screen)

    def draw_save_dialog(self, screen):
        # Рисуем фон окна и ввод для имени уровня
        pygame.draw.rect(screen, (50, 50, 50), self.dialog_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.input_rect)
        
        font = pygame.font.Font(None, 24)
        prompt_text = font.render("Введите имя уровня:", True, (255, 255, 255))
        screen.blit(prompt_text, (self.dialog_rect.x + 20, self.dialog_rect.y + 20))
        
        # Отображаем текст, введённый пользователем
        input_text = font.render(self.level_name, True, (0, 0, 0))
        screen.blit(input_text, (self.input_rect.x + 5, self.input_rect.y + 5))
