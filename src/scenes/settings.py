import pygame
from src.config import *
from resource_path import resource_path


class Settings:
    def __init__(self, game):
        self.game = game
        # Получаем доступ к SoundManager
        self.sound_manager = self.game.sound_manager
        self.options = [
            {'name': 'Громкость музыки', 'value': int(self.sound_manager.music_volume * 100), 'min': 0, 'max': 100},
            {'name': 'Громкость звуков', 'value': int(self.sound_manager.sound_volume * 100), 'min': 0, 'max': 100},
            {'name': 'Управление', 'action': self.show_controls},
            {'name': 'Назад', 'action': self.return_to_menu}
        ]
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)

        # Загружаем фон
        self.background_image = pygame.image.load(resource_path('assets/images/backgrounds/main_menu_background.png')).convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Загружаем настройки из файла
        self.load_settings()

        # Дополнительные атрибуты для подсветки кнопок
        self.hovered_option = None  # Индекс опции, над которой курсор мыши
        self.option_rects = []  # Прямоугольники опций для проверки нажатия


    def load_settings(self):
        self.options[0]['value'] = int(self.game.game_state.music_volume * 100)
        self.options[1]['value'] = int(self.game.game_state.sound_volume * 100)


    def save_settings(self):
        self.game.game_state.music_volume = self.options[0]['value'] / 100
        self.game.game_state.sound_volume = self.options[1]['value'] / 100


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.hovered_option = None  # Сбрасываем подсветку при наведении

            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                self.hovered_option = None  # Сбрасываем подсветку при наведении

            elif event.key == pygame.K_LEFT:
                self.adjust_value(-5)

            elif event.key == pygame.K_RIGHT:
                self.adjust_value(5)

            elif event.key == pygame.K_RETURN:
                option = self.options[self.selected_option]

                if 'action' in option:
                    option['action']()

        if event.type == pygame.MOUSEMOTION:
            self.hovered_option = None

            for i, option in enumerate(self.options):
                text = self.font.render(option['name'], True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))

                if text_rect.collidepoint(event.pos):
                    self.hovered_option = i
                    self.selected_option = i  # Обновляем selected_option при наведении мышкой
                    break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                for i, option in enumerate(self.options):
                    text = self.font.render(option['name'], True, WHITE)
                    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))

                    if text_rect.collidepoint(event.pos):
                        if 'action' in option:
                            option['action']()
                        else:  # Если это опция с 'value', то меняем её значение
                            self.adjust_value(0)  # Просто вызываем adjust_value, чтобы обновить значение
                        break

    def adjust_value(self, delta):
        option = self.options[self.selected_option]
        if 'value' in option:
            option['value'] = max(option['min'], min(option['max'], option['value'] + delta))
            self.apply_settings()

    def apply_settings(self):
        # Используем SoundManager для изменения громкости музыки и звуков
        self.sound_manager.set_music_volume(self.options[0]['value'] / 100)
        self.sound_manager.set_sound_volume(self.options[1]['value'] / 100)
        self.save_settings()  # Сохраняем изменения в файл

    def show_controls(self):
        # Показать экран с управлением
        pass

    def return_to_menu(self):
        from src.scenes.menu import MainMenu
        self.game.change_scene(MainMenu(self.game))

    def update(self):
        pass

    def draw(self, screen):
        # Отрисовка фона
        screen.blit(self.background_image, (0, 0))

        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected_option else WHITE  # Подсветка только для selected
            if 'value' in option:
                text = f"{option['name']}: {option['value']}%"
            else:
                text = option['name']
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))
            screen.blit(text_surface, text_rect)

    def show_controls(self):
        from src.scenes.controls_menu import ControlsMenu
        self.game.change_scene(ControlsMenu(self.game))