import pygame
from src.config import *


class SoundManager:
    def __init__(self, game):
        self.game = game
        self.sounds = {}
        self.music_volume = 1.0
        self.sound_volume = 1.0


    def play_sound(self, sound_name):
        sound_files = {
            'jump': 'jump.mp3',
            'coins': 'coins.mp3',
            'powerup': 'powerup.mp3',
            'death': 'death.mp3',
            'stomp': 'stomp.mp3',
            'block_hit':"block_hit.mp3"
        }

        try:
            sound = pygame.mixer.Sound(f'assets/musics/{sound_files[sound_name]}')
            self.sound_volume = self.game.game_state.sound_volume
            self.sounds[sound_name] = sound
            self.sounds[sound_name].set_volume(self.sound_volume)

        except pygame.error:
            print(f"Не удалось загрузить звук: {sound_name}")

        self.sounds[sound_name].play()

    def play_music(self, music_name):
        try:
            if not pygame.mixer.music.get_busy():  # Проверяем, играет ли музыка
                pygame.mixer.music.load(f'assets/musics/{music_name}.mp3')

                self.music_volume = self.game.game_state.music_volume

                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # -1 для бесконечного повтора
            else:
                pygame.mixer.music.fadeout(500)  # Плавное затухание текущей музыки (500 мс)
                pygame.mixer.music.load(f'assets/musics/{music_name}.mp3')
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)

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
