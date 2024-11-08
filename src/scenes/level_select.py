import os
import pygame
import json
from src.scenes.level import Level
from src.config import *

class LevelSelect:
    def __init__(self, game):
        self.game = game
        self.levels = self.get_available_levels()
        self.selected_level = 0  # Начинаем с первого уровня
        self.font = pygame.font.Font(None, 36)

        # Загружаем фон для меню выбора уровня
        self.background_image = pygame.image.load('assets/images/backgrounds/level_selected.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def get_available_levels(self):
        completed_levels = self.game.game_state.save_data['completed_levels']
        levels = []

        # Читаем JSON-файлы из папки levels
        for filename in os.listdir('levels'):
            if filename.endswith('.json'):
                with open(os.path.join('levels', filename), 'r') as f:
                    level_data = json.load(f)
                    level_name = filename[:-5]  # Имя файла без .json
                    status = "Пройден" if level_name in completed_levels else "Не пройден"
                    locked = len(levels) > 0 and levels[-1]['name'] not in completed_levels
                    levels.append({
                        'name': level_name,
                        'status': status,
                        'locked': locked,
                        'data': level_data  # Добавляем данные уровня
                    })

        return levels

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Находим предыдущий доступный уровень
                self.selected_level = max(0, self.selected_level - 1)
                while self.selected_level >= 0 and self.levels[self.selected_level]['locked']:
                    self.selected_level -= 1
            elif event.key == pygame.K_DOWN:
                # Находим следующий доступный уровень
                self.selected_level = (self.selected_level + 1) % len(self.levels)
                while self.levels[self.selected_level]['locked']:
                    self.selected_level = (self.selected_level + 1) % len(self.levels)
            elif event.key == pygame.K_RETURN:
                self.start_level()
            elif event.key == pygame.K_ESCAPE:
                from src.scenes.menu import MainMenu
                self.game.change_scene(MainMenu(self.game))

    def start_level(self):
        level = self.levels[self.selected_level]
        if not level['locked']:
            self.game.change_scene(Level(self.game, level['name'], level['data']))

    def update(self):
        pass

    def draw(self, screen):
        # Отрисовка фона
        screen.blit(self.background_image, (0, 0))

        for i, level in enumerate(self.levels):
            color = GREEN if i == self.selected_level else WHITE
            if level['locked']:
                color = (100, 100, 100)  # Серый для заблокированных уровней

            text = f"{level['name']} - {level['status']}"
            if level['locked']:
                text += " (Заблокирован)"

            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))
            screen.blit(text_surface, text_rect)