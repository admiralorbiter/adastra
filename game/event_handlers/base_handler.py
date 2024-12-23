class BaseEventHandler:
    def __init__(self, game_state):
        self.game_state = game_state

    def handle_event(self, event):
        """Base method to handle a pygame event"""
        pass 