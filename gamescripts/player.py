#game/player.py
from .entity import Entity
from .game_state_manager import GameStateManager

class Player(Entity):
    def __init__(self, name, health=100):
        super().__init__(name, health)
    
    def set_player_position(game_state=None, new_position=(0, 0)):
        if not game_state:
            game_state = GameStateManager.get()

        try:
            game_state["player_location"]["player_position"] = new_position
            world = game_state["player_location"]["current_world"]
            tile = world.get_tile(*new_position)
            game_state["player_location"]["current_tile"] = tile
            GameStateManager.set(game_state)
        except Exception as e:
            print(f"Could not change player position: {e}")
