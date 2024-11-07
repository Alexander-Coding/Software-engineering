import sys
sys.path.append(r'C:\Users\Alexa\github\BioSense\mario\src')
import pygame
import json
from config import *
from entities.player import Player
from entities.enemy import Enemy
from entities.block import Block

class Level:
    def __init__(self, game, level_id):
        self.game = game
        self.level_id = level_id
        self.camera_x = 0
        
        # Группы спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        self.player = None
        self.load_level()
        
    def load_level(self):
        try:
            with open(f'levels/level_{self.level_id}.json', 'r') as f:
                level_data = json.load(f)
                
            for obj in level_data:
                if obj['type'] == 'spawn':
                    self.player = Player(obj['x'], obj['y'])
                    self.all_sprites.add(self.player)
                elif obj['type'] == 'block':
                    block = Block(obj['x'], obj['y'], obj['type'])
                    self.blocks.add(block)
                    self.all_sprites.add(block)
                elif obj['type'] == 'enemy':
                    enemy = Enemy(obj['x'], obj['y'], obj['type'])
                    self.enemies.add(enemy)
                    self.all_sprites.add(enemy)
                    
        except FileNotFoundError:
            print(f"Уровень {self.level_id} не найден")
            
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.pause_game()
                
    def pause_game(self):
        self.game.is_paused = True
        # Показать меню паузы
                
    def update(self):
            
        self.all_sprites.update()
        self.handle_collisions()
        self.update_camera()
        
    def handle_collisions(self):
        # Коллизии с блоками
        hits = pygame.sprite.spritecollide(self.player, self.blocks, False)
        for block in hits:
            if self.player.velocity_y > 0:
                self.player.rect.bottom = block.rect.top
                self.player.velocity_y = 0
                self.player.on_ground = True
            elif self.player.velocity_y < 0:
                self.player.rect.top = block.rect.bottom
                self.player.velocity_y = 0
                
        # Коллизии с врагами
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            if self.player.velocity_y > 0:
                enemy.kill()
                self.player.velocity_y = -10
            else:
                self.player_hit()
                
    def player_hit(self):
        if not self.player.is_invincible:
            if self.player.is_big:
                self.player.is_big = False
            else:
                self.game_over()
                
    def game_over(self):
        # Показать экран game over
        pass
        
    def update_camera(self):
        target_x = self.player.rect.centerx - WINDOW_WIDTH // 2
        self.camera_x += (target_x - self.camera_x) * 0.1
        
    def draw(self, screen):
        screen.fill((107, 140, 255))  # Цвет неба
        
        for sprite in self.all_sprites:
            screen.blit(sprite.image, 
                       (sprite.rect.x - self.camera_x, sprite.rect.y))
        