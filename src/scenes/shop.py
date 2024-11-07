import pygame
from src.utils.save_system import SaveSystem
from src.config import *

class Shop:
    def __init__(self, game):
        self.game = game
        self.items = [
            {'name': 'Классический Марио', 'cost': 0, 'id': 'default'},
            {'name': 'Огненный Марио', 'cost': 1000, 'id': 'fire'},
            {'name': 'Ледяной Марио', 'cost': 2000, 'id': 'ice'},
            {'name': 'Золотой Марио', 'cost': 5000, 'id': 'gold'}
        ]
        self.selected_item = 0
        self.font = pygame.font.Font(None, 36)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                self.buy_item()
            elif event.key == pygame.K_ESCAPE:
                from src.scenes.menu import MainMenu
                self.game.change_scene(MainMenu(self.game))
                
    def buy_item(self):
        item = self.items[self.selected_item]
        if (item['id'] not in self.game.game_state.save_data['unlocked_skins'] and 
            self.game.game_state.save_data['score'] >= item['cost']):
            self.game.game_state.save_data['score'] -= item['cost']
            self.game.game_state.save_data['unlocked_skins'].append(item['id'])
            SaveSystem.save_game(self.game.game_state.save_data)
            
    def update(self):
        pass
        
    def draw(self, screen):
        screen.fill(BLACK)
        
        # Отображение счета
        score_text = self.font.render(
            f"Очки: {self.game.game_state.save_data['score']}", 
            True, WHITE
        )
        screen.blit(score_text, (20, 20))
        
        # Отображение предметов
        for i, item in enumerate(self.items):
            color = GREEN if i == self.selected_item else WHITE
            status = "Куплено" if item['id'] in self.game.game_state.save_data['unlocked_skins'] else f"Цена: {item['cost']}"
            
            text = self.font.render(f"{item['name']} - {status}", True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 200 + i * 50))
            screen.blit(text, text_rect)