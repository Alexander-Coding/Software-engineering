import pygame
from src.config import *

class Settings:
    def __init__(self, game):
        self.game = game
        self.options = [
            {'name': 'Громкость музыки', 'value': 100, 'min': 0, 'max': 100},
            {'name': 'Громкость звуков', 'value': 100, 'min': 0, 'max': 100},
            {'name': 'Управление', 'action': self.show_controls},
            {'name': 'Назад', 'action': self.return_to_menu}
        ]
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_LEFT:
                self.adjust_value(-5)
            elif event.key == pygame.K_RIGHT:
                self.adjust_value(5)
            elif event.key == pygame.K_RETURN:
                option = self.options[self.selected_option]
                if 'action' in option:
                    option['action']()
                    
    def adjust_value(self, delta):
        option = self.options[self.selected_option]
        if 'value' in option:
            option['value'] = max(option['min'], min(option['max'], option['value'] + delta))
            self.apply_settings()
            
    def apply_settings(self):
        pygame.mixer.music.set_volume(self.options[0]['value'] / 100)
        # Применить другие настройки
        
    def show_controls(self):
        # Показать экран с управлением
        pass
        
    def return_to_menu(self):
        from src.scenes.menu import MainMenu
        self.game.change_scene(MainMenu(self.game))
        
    def update(self):
        pass
        
    def draw(self, screen):
        screen.fill(BLACK)
        
        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected_option else WHITE
            
            if 'value' in option:
                text = f"{option['name']}: {option['value']}%"
            else:
                text = option['name']
                
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))
            screen.blit(text_surface, text_rect)