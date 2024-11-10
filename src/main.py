import pygame
import sys
from src.config import *
from scenes.menu import MainMenu
from game_state import GameState
from src.utils import SoundManager
from src.scenes import LevelSelect


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.sound_manager = SoundManager()
        self.sound_manager.play_music('Super_Mario')
        self.game_state = GameState()
        self.current_scene = MainMenu(self)
        
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
    def handle_events(self):
         for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.quit()
                return

            self.current_scene.handle_event(event)
    
    def update(self):
        self.current_scene.update()
                
    def draw(self):
        self.current_scene.draw(self.screen)
        pygame.display.flip()
                
    def quit(self):
        pygame.quit()
        sys.exit()
    
    def change_scene(self, scene):
        self.current_scene = scene

    def level_complete(self):
        self.change_scene(LevelSelect(self))

if __name__ == "__main__":
    game = Game()
    game.run()