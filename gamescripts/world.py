#game/world.py
from enum import Enum
import random

class WorldTypes(Enum):
    NORMAL = 1
    CELESTIAL = 2
    ABYSSAL = 3
    PANGEA = 4
    ARCHIPELAGO = 5
    CLAUSTROPHOBIA = 6

class Biome(Enum):
    PLAINS = "Plains"
    FOREST = "Forest"
    DESERT = "Desert"
    MOUNTAINS = "Mountains"
    SWAMP = "Swamp"
    OCEAN = "Ocean"

class Tile:
    def __init__(self, x, y, biome, altitude):
        self.x = x
        self.y = y
        self.biome = biome
        self.altitude = altitude

    def describe(self):
        return f"Tile ({self.x}, {self.y}) - {self.biome.value}, Altitude: {self.altitude}"

class World:
    def __init__(self, name, width=10, height=10, worldType=WorldTypes.NORMAL):
        self.name = name
        self.worldType = worldType
        self.width = width
        self.height = height
        self.tiles = WorldGenerator.generate(width, height, WorldTypes.NORMAL)
    
    def get_tile(self, x, y):
        return self.tiles.get((x, y))
    
class WorldGenerator:
    @classmethod
    def generate(cls, width, height, worldType):
        if worldType == WorldTypes.NORMAL:
            return cls._generate_normal_world(width, height)
    
    @classmethod
    def _generate_normal_world(cls, width, height):
        worldTiles = {}
        for x in range(width):
            for y in range(height):
                biome = random.choice(list(Biome))
                altitude = random.randint(0, 100)
                tile = Tile(x, y, biome, altitude)
                worldTiles[(x, y)] = tile
        return worldTiles

"""
myWorld = World("World 1")
print(f"World: {myWorld.name}")
print(f"Tile count: {len(myWorld.tiles)}")
for coords, tile in myWorld.tiles.items():
    print(f"{coords}: {tile.describe()}")
"""
