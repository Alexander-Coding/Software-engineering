from utils.save_system import SaveSystem

class GameState:
    def __init__(self):
        self.save_data = SaveSystem.load_game()
        self.current_level = None
        self.is_paused = False
        
    @property
    def score(self):
        return self.save_data['score']
    
    @score.setter
    def score(self, value):
        self.save_data['score'] = value
        SaveSystem.save_game(self.save_data)
    
    def complete_level(self, level_id):
        if level_id not in self.save_data['completed_levels']:
            self.save_data['completed_levels'].append(level_id)
            SaveSystem.save_game(self.save_data)
    
    def is_level_completed(self, level_id):
        return level_id in self.save_data['completed_levels']