#game/world.py
from enum import Enum

class WorldTypes:
    NORMAL = 1
    CELESTIAL = 2
    ABYSSAL = 3
    PANGEA = 4
    ARCHIPELAGO = 5
    CLAUSTROPHOBIA = 6

class World:
    def __init__(self, name, worldType=WorldTypes.NORMAL):
        self.name = name
        self.worldType = worldType

def send(object, target):
    pass