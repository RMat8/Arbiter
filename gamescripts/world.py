#game/world.py
from enum import Enum
import random
import hashlib

#modules
from .game_state_manager import GameStateManager
from .colors import *

def pseudo_noise(x, y, seed=0, base_altitude=50, variance=10, spike_chance=0.02, spike_height=30):
    key = f"{x},{y},{seed}".encode()
    hash_val = hashlib.md5(key).hexdigest()
    noise_val = int(hash_val[:4], 16) / 0xFFFF

    variation = (noise_val - 0.5) * 2 * variance  # -variance to +variance
    altitude = int(base_altitude + variation)

    if noise_val > (1.0 - spike_chance):
        altitude += spike_height
    elif noise_val < spike_chance:
        altitude -= spike_height

    return max(0, min(100, altitude))

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
    
    def print_altitude_map(self):
        print("\n")
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                tile = self.get_tile(x, y)
                if tile:
                    color = blue_shade(tile.altitude)
                    row += f"{color}{tile.altitude:3}{RESET}"
                else:
                    row += " ?  "
            print(row)
        return "\n"

class WorldGenerator:
    @classmethod
    def generate(cls, width, height, worldType, seed=1234):
        if worldType == WorldTypes.NORMAL:
            return cls._generate_normal_world(width, height, seed)
    
    @classmethod
    def _generate_normal_world(cls, width, height, seed):
        worldTiles = {}
        for x in range(width):
            for y in range(height):
                biome = random.choice(list(Biome))
                altitude = cls._pseudo_noise(x, y, seed)
                tile = Tile(x, y, biome, altitude)
                worldTiles[(x, y)] = tile
        return worldTiles
    
    @staticmethod
    def _pseudo_noise(x, y, seed):
        return pseudo_noise(x, y, 
                            seed, base_altitude=50, 
                            variance=8, 
                            spike_chance=0.12, #0.015
                            spike_height=25)

"""
myWorld = World("World 1")
print(f"World: {myWorld.name}")
print(f"Tile count: {len(myWorld.tiles)}")
for coords, tile in myWorld.tiles.items():
    print(f"{coords}: {tile.describe()}")
"""
