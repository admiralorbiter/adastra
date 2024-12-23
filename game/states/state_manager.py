from typing import Optional, Callable
from .game_states import GameState

class StateManager:
    def __init__(self):
        self._current_state: GameState = GameState.PLAYING
        self._previous_state: Optional[GameState] = None
        self._state_handlers: dict[GameState, Callable] = {}
        self._state_enter_handlers: dict[GameState, Callable] = {}
        self._state_exit_handlers: dict[GameState, Callable] = {}
    
    @property
    def current_state(self) -> GameState:
        return self._current_state
    
    def register_state_handler(self, state: GameState, handler: Callable) -> None:
        """Register a handler function for a specific state"""
        self._state_handlers[state] = handler
        
    def register_state_enter_handler(self, state: GameState, handler: Callable) -> None:
        """Register a handler function called when entering a state"""
        self._state_enter_handlers[state] = handler
        
    def register_state_exit_handler(self, state: GameState, handler: Callable) -> None:
        """Register a handler function called when exiting a state"""
        self._state_exit_handlers[state] = handler
    
    def change_state(self, new_state: GameState) -> None:
        """Change to a new state"""
        if new_state == self._current_state:
            return
            
        # Call exit handler for current state
        if self._current_state in self._state_exit_handlers:
            self._state_exit_handlers[self._current_state]()
            
        self._previous_state = self._current_state
        self._current_state = new_state
        
        # Call enter handler for new state
        if new_state in self._state_enter_handlers:
            self._state_enter_handlers[new_state]()
    
    def update(self, dt: float) -> None:
        """Update current state"""
        if self._current_state in self._state_handlers:
            self._state_handlers[self._current_state](dt)
    
    def revert_to_previous_state(self) -> None:
        """Revert to the previous state if one exists"""
        if self._previous_state:
            self.change_state(self._previous_state) 