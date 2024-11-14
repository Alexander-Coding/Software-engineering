import pygame
from src.config import *
from resource_path import resource_path


class ControlsMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)

        # Загружаем фон
        self.background_image = pygame.image.load(resource_path('assets/images/backgrounds/main_menu_background.png')).convert_alpha()
        # Замените 'assets/images/backgrounds/controls_background.png' на фактический путь к вашему файлу фона
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Загружаем изображение с управлением
        self.controls_image = pygame.image.load(resource_path('assets/images/backgrounds/key.png')).convert_alpha()
        # Замените 'assets/images/controls.png' на фактический путь к вашему файлу изображения с управлением
        self.controls_image = pygame.transform.scale(self.controls_image, (400, 300))

        # Добавляем логику выбора
        self.selected = False  # Кнопка "Назад" не выбрана по умолчанию
        self.hovered = False  # Кнопка "Назад" не выделена при наведении по умолчанию

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.return_to_settings()
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.selected = not self.selected
                self.hovered = False  # Сбрасываем подсветку при наведении

        if event.type == pygame.MOUSEMOTION:
            text = self.font.render("Назад", True, WHITE)  # Отрисовываем текст для определения области
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
            if text_rect.collidepoint(event.pos):
                self.hovered = True
                self.selected = True  # Выбираем кнопку при наведении
            else:
                self.hovered = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                text = self.font.render("Назад", True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
                if text_rect.collidepoint(event.pos):
                    self.return_to_settings()

    def return_to_settings(self):
        from src.scenes.settings import Settings
        self.game.change_scene(Settings(self.game))

    def update(self):
        pass

    def draw(self, screen):
        # Отрисовка фона
        screen.blit(self.background_image, (0, 0))

        # Отрисовка изображения с управлением
        controls_rect = self.controls_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(self.controls_image, controls_rect)

        # Отрисовка кнопки "Назад" с выделением
        text = self.font.render("Назад", True, GREEN if self.selected or self.hovered else WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
        screen.blit(text, text_rect)