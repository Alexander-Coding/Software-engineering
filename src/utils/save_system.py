import json
import os
from src.config import SAVE_FILE


class SaveSystem:
    @staticmethod
    def save_game(data):
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f)
            return True
        
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return

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

        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f)

        return data

    @staticmethod
    def load_game():
        if not os.path.exists(SAVE_FILE):
            data = {
                'completed_levels': [],
                'score': 0,
                'live': 3,
                'coins': 0,
                'sound_volume': 0,
                'music_volume': 0,
                'mario_is_big': False
            }

            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f)

            return data
        
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
            
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return None