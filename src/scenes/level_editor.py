import pygame
import json
import os

import sys
sys.path.append(r'C:\Users\Alexa\github\BioSense\mario\src')
from pathlib import Path
from config import *
from pygame.locals import *

class LevelEditor:
    def __init__(self, game):
        self.game = game
        self.grid_size = 32
        self.current_tile = None
        self.tiles = {}
        self.level_data = []
        self.camera_x = 0
        self.asset_list_rect = pygame.Rect(WINDOW_WIDTH - 200, 0, 200, WINDOW_HEIGHT)
        self.asset_buttons = []
        self.scroll_y = 0
        self.load_assets()
        
        # Кнопка сохранения уровня
        self.save_button_rect = pygame.Rect(10, WINDOW_HEIGHT - 50, 100, 40)
        
        # Параметры диалогового окна
        self.showing_save_dialog = False
        self.level_name = ""
        self.dialog_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 75, 300, 150)
        self.input_rect = pygame.Rect(self.dialog_rect.x + 20, self.dialog_rect.y + 60, 260, 30)

    def load_assets(self):
        assets_path = Path('assets')
        for asset_file in assets_path.rglob('*.png'):
            asset_name = asset_file.stem
            image = pygame.image.load(str(asset_file))
            aspect_ratio = image.get_width() / image.get_height()
            if aspect_ratio > 1:
                new_width = self.grid_size
                new_height = int(self.grid_size / aspect_ratio)
            else:
                new_width = int(self.grid_size * aspect_ratio)
                new_height = self.grid_size
            
            self.tiles[asset_name] = pygame.transform.scale(image, (new_width, new_height))
            button_rect = pygame.Rect(WINDOW_WIDTH - 180, len(self.asset_buttons) * 40 + 10, 160, 32)
            self.asset_buttons.append({'rect': button_rect, 'name': asset_name})

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
                if self.save_button_rect.collidepoint(mouse_pos):
                    # Нажатие на кнопку сохранения
                    self.showing_save_dialog = True
                elif self.asset_list_rect.collidepoint(mouse_pos):
                    adjusted_y = mouse_pos[1] + self.scroll_y
                    for button in self.asset_buttons:
                        if button['rect'].collidepoint(mouse_pos[0], adjusted_y):
                            self.current_tile = button['name']
                            break
                else:
                    if self.current_tile:
                        self.place_tile()
            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_y = max(0, min(self.scroll_y - event.y * 20, 
                    max(0, len(self.asset_buttons) * 40 - WINDOW_HEIGHT)))

    def place_tile(self):
        mouse_pos = pygame.mouse.get_pos()
        grid_x = (mouse_pos[0] + self.camera_x) // self.grid_size
        grid_y = mouse_pos[1] // self.grid_size
        
        tile_data = {
            'asset_name': self.current_tile,
            'type': 'block',
            'x': grid_x * self.grid_size,
            'y': grid_y * self.grid_size
        }
        
        self.level_data.append(tile_data)
        
    def save_level(self, name):
        os.makedirs('levels', exist_ok=True)
        filename = f'levels/{name}.json'
        
        with open(filename, 'w') as f:
            json.dump(self.level_data, f)
        print(f"Уровень сохранен как {filename}")

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_x = max(0, self.camera_x - 5)
        if keys[pygame.K_RIGHT]:
            self.camera_x += 5
            
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
            screen.blit(self.tiles[tile['asset_name']], 
                       (tile['x'] - self.camera_x, tile['y']))
            
        pygame.draw.rect(screen, (200, 200, 200), self.asset_list_rect)
        
        for button in self.asset_buttons:
            button_rect = button['rect'].copy()
            button_rect.y -= self.scroll_y
            if self.asset_list_rect.contains(button_rect):
                color = (150, 150, 150) if button['name'] == self.current_tile else (220, 220, 220)
                pygame.draw.rect(screen, color, button_rect)
                screen.blit(self.tiles[button['name']], 
                          (button_rect.x + 5, button_rect.y + 2))
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
