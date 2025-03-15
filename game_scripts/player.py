#game/player.py
from game_scripts.entity import Entity
class Player(Entity):
    def __init__(self, name=..., health=100):
        super().__init__(name, health)
        self.inventory = {}
        