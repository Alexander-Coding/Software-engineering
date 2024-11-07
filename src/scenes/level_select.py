import pygame
import sys
sys.path.append(r'C:\Users\Alexa\github\BioSense\mario\src')

from scenes.level import Level
from config import *

class LevelSelect:
    def __init__(self, game):
        self.game = game
        self.levels = self.get_available_levels()
        self.selected_level = 1
        self.font = pygame.font.Font(None, 36)
        
    def get_available_levels(self):
        completed_levels = self.game.game_state.save_data['completed_levels']
        levels = []
        
        for i in range(1, 6):  # Предположим, у нас 5 уровней
            status = "Пройден" if i in completed_levels else "Не пройден"
            locked = i > 1 and (i-1) not in completed_levels
            levels.append({
                'id': i,
                'name': f"Уровень {i}",
                'status': status,
                'locked': locked
            })

        return levels
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_level = (self.selected_level - 1) % len(self.levels)
            elif event.key == pygame.K_DOWN:
                self.selected_level = (self.selected_level + 1) % len(self.levels)
            elif event.key == pygame.K_RETURN:
                self.start_level()
            elif event.key == pygame.K_ESCAPE:
                from scenes.menu import MainMenu
                self.game.change_scene(MainMenu(self.game))
                
    def start_level(self):
        level = self.levels[self.selected_level]
        if not level['locked']:
            self.game.change_scene(Level(self.game, level['id']))
        
    def update(self):
        pass
        
    def draw(self, screen):
        screen.fill(BLACK)
        
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
