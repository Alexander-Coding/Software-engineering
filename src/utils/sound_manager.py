import pygame
import sys
sys.path.append(r'C:\Users\Alexa\github\BioSense\mario\src')
from config import *

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_volume = 1.0
        self.sound_volume = 1.0
        self.load_sounds()
        
    def load_sounds(self):
        sound_files = {
            # 'jump': 'jump.wav',
            # 'coin': 'coin.wav',
            # 'powerup': 'powerup.wav',
            # 'death': 'death.wav',
            # 'stomp': 'stomp.wav',
            # 'break': 'break.wav'
        }
        
        for sound_name, file_name in sound_files.items():
            try:
                sound = pygame.mixer.Sound(f'assets/sounds/{file_name}')
                self.sounds[sound_name] = sound
            except pygame.error:
                print(f"Не удалось загрузить звук: {file_name}")
                
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(self.sound_volume)
            self.sounds[sound_name].play()
            
    def play_music(self, music_name):
        try:
            pygame.mixer.music.load(f'assets/music/{music_name}.mp3')
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # -1 для бесконечного повтора
        except pygame.error:
            print(f"Не удалось загрузить музыку: {music_name}")
            
    def stop_music(self):
        pygame.mixer.music.stop()
        
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        
    def set_sound_volume(self, volume):
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)