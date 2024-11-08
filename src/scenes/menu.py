import pygame
from src.config import *

import pygame
from src.config import *


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.sound_manager = self.game.sound_manager
        self.buttons = [
            {'text': 'Играть', 'action': self.start_game},
            {'text': 'Редактор уровней', 'action': self.open_editor},
            {'text': 'Настройки', 'action': self.open_settings},
            {'text': 'Выход', 'action': self.game.quit}
        ]
        self.selected = 0
        self.font = pygame.font.Font(None, 36)

        # Загружаем фон
        self.background_image = pygame.image.load('assets/images/backgrounds/main_menu_background.png').convert_alpha()

        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selected]['action']()
    def update(self):
        pass

    def draw(self, screen):
        # Отрисовка фона
        screen.blit(self.background_image, (0, 0))

        for i, button in enumerate(self.buttons):
            color = GREEN if i == self.selected else WHITE
            text = self.font.render(button['text'], True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))
            screen.blit(text, text_rect)

    def start_game(self):
        from src.scenes.level_select import LevelSelect

        self.game.change_scene(LevelSelect(self.game))

    def open_editor(self):
        from src.scenes.level_editor import LevelEditor
        self.game.change_scene(LevelEditor(self.game))

    def open_settings(self):
        from src.scenes.settings import Settings
        self.game.change_scene(Settings(self.game))