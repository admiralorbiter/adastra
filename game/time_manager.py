import time

class TimeManager:
    def __init__(self):
        self.time_scale = 1.0
        self.paused = False
        self.game_time = 0  # Time in seconds
        
    def update(self, dt):
        if not self.paused:
            self.game_time += dt * self.time_scale
            
    def set_time_scale(self, scale):
        self.time_scale = scale
        
    def toggle_pause(self):
        self.paused = not self.paused
        
    def get_scaled_dt(self, dt):
        if self.paused:
            return 0
        return dt * self.time_scale
        
    def get_time_string(self):
        total_minutes = int(self.game_time / 60)
        hours = (total_minutes // 60) % 24
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}" 