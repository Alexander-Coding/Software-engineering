import pygame
import json
from src.config import *
from src.utils import SaveSystem


class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.sound_manager = self.game.sound_manager
        self.buttons = [
            {'text': 'Главное меню', 'action': self.go_to_main_menu},
            {'text': 'Начать заново', 'action': self.restart_level},
            {'text': 'Продолжить', 'action': self.resume_game},
        ]
        self.selected = 0
        self.font = pygame.font.Font(None, 36)

        # Загружаем фон
        self.background_image = pygame.image.load('assets/images/backgrounds/sky.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Дополнительные атрибуты для подсветки кнопок
        self.hovered_button = None
        self.button_rects = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
                self.hovered_button = None
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
                self.hovered_button = None
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selected]['action']()

        if event.type == pygame.MOUSEMOTION:
            self.hovered_button = None
            for i, button in enumerate(self.buttons):
                text = self.font.render(button['text'], True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 300 + i * 50))
                if text_rect.collidepoint(event.pos):
                    self.hovered_button = i
                    self.selected = i
                    break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, button in enumerate(self.buttons):
                    text = self.font.render(button['text'], True, WHITE)
                    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 300 + i * 50))
                    if text_rect.collidepoint(event.pos):
                        button['action']()
                        break

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))

        # Отрисовка заголовка
        title_font = pygame.font.Font(None, 60)
        title_text = title_font.render("Пауза", True, RED)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Отрисовка кнопок
        for i, button in enumerate(self.buttons):
            color = GREEN if i == self.selected else WHITE
            text = self.font.render(button['text'], True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 300 + i * 50))
            screen.blit(text, text_rect)

    def go_to_main_menu(self):
        from src.scenes.menu import MainMenu
        self.game.change_scene(MainMenu(self.game))

    def restart_level(self):
        self.game.current_scene.reset_level()
        self.game.change_scene(self.game.current_scene)

    def resume_game(self):
        self.game.is_paused = False
        self.game.change_scene(self.game.current_scene)  # Возвращаемся к текущей игре

