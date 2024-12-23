import time

class TimeManager:
    def __init__(self):
        self.time_scale = 1.0
        self.paused = False
        self.game_time = 0  # Time in seconds
        
        # Constants for time conversion
        self.REAL_MINUTES_PER_DAY = 6.0  # 6 minutes real time = 24 hours game time
        self.GAME_SECONDS_PER_DAY = 24 * 60 * 60  # 24 hours in seconds
        self.TIME_MULTIPLIER = self.GAME_SECONDS_PER_DAY / (self.REAL_MINUTES_PER_DAY * 60)
        
    def update(self, dt):
        if not self.paused:
            # Apply time multiplier and scale
            self.game_time += dt * self.TIME_MULTIPLIER * self.time_scale
            # Wrap around to keep within 24 hours
            self.game_time %= self.GAME_SECONDS_PER_DAY
            
    def set_time_scale(self, scale):
        self.time_scale = scale
        
    def toggle_pause(self):
        self.paused = not self.paused
        
    def get_scaled_dt(self, dt):
        if self.paused:
            return 0
        return dt * self.time_scale
        
    def get_time_string(self):
        total_seconds = int(self.game_time)
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}" 