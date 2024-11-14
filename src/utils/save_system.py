import json
import os
from src.config import SAVE_FILE
from resource_path import resource_path


class SaveSystem:
    @staticmethod
    def save_game(data):
        with open(resource_path(SAVE_FILE), 'w') as f:
            json.dump(data, f)

        return True

    @staticmethod
    def reset_game():
        data = {
            'completed_levels': [],
            'score': 0,
            'live': 3,
            'coins': 0,
            'sound_volume': 0,
            'music_volume': 0,
            'mario_is_big': False
        }

        with open(resource_path(SAVE_FILE), 'w') as f:
            json.dump(data, f)

        return data

    @staticmethod
    def load_game():
        if not os.path.exists(resource_path(SAVE_FILE)):
            data = {
                'completed_levels': [],
                'score': 0,
                'live': 3,
                'coins': 0,
                'sound_volume': 0,
                'music_volume': 0,
                'mario_is_big': False
            }

            with open(resource_path(SAVE_FILE), 'w') as f:
                json.dump(data, f)

            return data
        
        with open(resource_path(SAVE_FILE), 'r') as f:
            return json.load(f)