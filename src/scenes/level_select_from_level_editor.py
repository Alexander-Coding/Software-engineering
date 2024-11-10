import os
import json
import pygame
from src.config import *
from src.scenes import LevelEditor


class LevelSelectorFromLevelEditor:
    def __init__(self, game):
        self.game = game
        self.levels = self.get_levels()
        self.selected_level = 0  # Начинаем с первого уровня
        self.font = pygame.font.Font(None, 36)

        # Загружаем фон для меню выбора уровня
        self.background_image = pygame.image.load('assets/images/backgrounds/level_selected.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Создаем прямоугольники для каждого уровня
        self.level_rects = []

        for i, level in enumerate(self.levels):
            text_surface = self.font.render(f"{level['name']}", True, WHITE)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))
            self.level_rects.append(text_rect)


    def get_levels(self):
        levels = [{
                'name': 'Новый уровень',
                'data': []
            }]

        for filename in os.listdir('levels'):
            if filename.endswith('.json'):
                with open(os.path.join('levels', filename), 'r') as f:
                    level_data = json.load(f)
                    level_name = filename[:-5]
                    levels.append({
                        'name': level_name,
                        'data': level_data
                    })

        return levels
    

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_level = max(0, self.selected_level - 1)

                while self.selected_level >= 0:
                    self.selected_level -= 1

            elif event.key == pygame.K_DOWN:
                # Находим следующий доступный уровень
                self.selected_level = (self.selected_level + 1) % len(self.levels)

            elif event.key == pygame.K_RETURN:
                self.start_level()

            elif event.key == pygame.K_ESCAPE:
                from src.scenes.menu import MainMenu
                self.game.change_scene(MainMenu(self.game))

        if event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.level_rects):
                if rect.collidepoint(event.pos):
                    self.selected_level = i
                    break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(self.level_rects):
                    if rect.collidepoint(event.pos):  # Проверка блокировки
                        self.start_level()
                        break


    def start_level(self):
        level = self.levels[self.selected_level]
        self.game.change_scene(LevelEditor(self.game, level['name'], level['data']))


    def update(self):
        pass


    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))

        for i, level in enumerate(self.levels):
            color = GREEN if i == self.selected_level else WHITE

            text = f"{level['name']}"

            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))

            screen.blit(text_surface, text_rect)