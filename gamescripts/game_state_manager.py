#gamescripts/game_state_manager.py
class GameStateManager:
    _state = None

    @classmethod
    def get(cls):
        return cls._state
    
    @classmethod
    def set(cls, game_state):
        cls._state = game_state
    
    @classmethod
    def reset(cls):
        cls._state = None
