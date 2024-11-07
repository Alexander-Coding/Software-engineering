class ScoringSystem:
    def __init__(self, game_state):
        self.game_state = game_state
        self.score_values = {
            'coin': 100,
            'enemy': 200,
            'powerup': 1000,
            'flag': 5000,
            'time_bonus': 50  # за каждую оставшуюся секунду
        }
        
    def add_score(self, score_type):
        if score_type in self.score_values:
            current_score = self.game_state.save_data['score']
            self.game_state.save_data['score'] = current_score + self.score_values[score_type]
            
    def add_coins(self, amount=1):
        current_coins = self.game_state.save_data['coins']
        self.game_state.save_data['coins'] = current_coins + amount
        
        # Каждые 100 монет дают дополнительную жизнь
        if self.game_state.save_data['coins'] >= 100:
            self.game_state.save_data['coins'] -= 100
            self.add_life()
            
    def add_life(self):
        self.game_state.save_data['lives'] += 1
        
    def calculate_time_bonus(self, remaining_time):
        bonus = remaining_time * self.score_values['time_bonus']
        self.add_score('time_bonus')
        return bonus