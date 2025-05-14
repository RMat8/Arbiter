#game/player.py
from gamescripts.entity import Entity

class Player(Entity):
    def __init__(self, name, health=100):
        super().__init__(name, health)
