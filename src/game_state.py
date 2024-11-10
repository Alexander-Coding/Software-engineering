from utils.save_system import SaveSystem


class GameState:
    def __init__(self):
        self.save_data = SaveSystem.load_game()
        self.current_level = None
        self.is_paused = False
        
    @property
    def score(self):
        return self.save_data['score']
    
    @property
    def live(self):
        return self.save_data['live']
    
    @property
    def coins(self):
        return self.save_data['coins']
    
    @property
    def music_volume(self):
        return self.save_data['music_volume']
        
    @property
    def sound_volume(self):
        return self.save_data['sound_volume']
    
    @property
    def coins(self):
        return self.save_data['coins']
    
    @score.setter
    def score(self, value):
        self.save_data['score'] = value
        SaveSystem.save_game(self.save_data)

    @music_volume.setter
    def music_volume(self, value):
        if value >= 0 and value <= 1:
            self.save_data['music_volume'] = value
            SaveSystem.save_game(self.save_data)

    @sound_volume.setter
    def sound_volume(self, value):
        if value >= 0 and value <= 1:
            self.save_data['sound_volume'] = value
            SaveSystem.save_game(self.save_data)

    @live.setter
    def live(self, value):
        if self.save_data['score'] <= 3 and value > 0 and value < 3:
            self.save_data['score'] = value
            SaveSystem.save_game(self.save_data)

    @coins.setter
    def coins(self, value):
        if value >= 0:
            if value >= 100 and self.save_data['live'] < 3:
                self.save_data['live'] += 1
                value = value - 100

            self.save_data['coins'] = value
            SaveSystem.save_game(self.save_data)
    
    def complete_level(self, level_id):
        if level_id not in self.save_data['completed_levels']:
            self.save_data['completed_levels'].append(level_id)
            SaveSystem.save_game(self.save_data)
    
    def is_level_completed(self, level_id):
        return level_id in self.save_data['completed_levels']