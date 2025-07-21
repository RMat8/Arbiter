#game/world.py
import os
import json
from enum import Enum, auto
import random

#modules
from .game_state_manager import GameStateManager
from .colors import *
from .noise import layered_noise
from .time import GameTime

class HostilityLevel(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    EXTREME = 4
    NIGHTMARE1 = 5
    #secret difficulty levels below
    NIGHTMARE2 = 6
    NIGHTMARE3 = 7
    NIGHTMARE4 = 8

def get_altitude(x, y, seed=0):
    val = layered_noise(x, y, seed, scale=0.02, octaves=8) #scale=0.03
    return int(val * 100) + 19

class WorldTypes(Enum):
    NORMAL = 1
    CELESTIAL = 2
    ABYSSAL = 3
    PANGEA = 4
    ARCHIPELAGO = 5
    CLAUSTROPHOBIA = 6

class Biome(Enum):
    #Polar
    ICECAP = "Icecap"
    TUNDRA = "Tundra"

    #Arid
    DESERT = "Desert"
    STEPPE = "Steppe"

    #Temperate
    PLAINS = "Plains"
    FOREST = "Forest"
    HILLS = "Hills"
    WETLANDS = "Wetlands"

    #Tropical
    RAINFOREST = "Rainforest"
    SAVANNA = "Savanna"
    JUNGLE = "Jungle"
    MANGROVE = "Mangrove"

    #Aquatic
    OCEAN = "Ocean"
    LAKE = "Lake"
    RIVER = "River"
    SWAMP = "Swamp"
    MARSH = "Marsh"

    #Mountainous
    ALPINE = "Alpine"
    ROCKY_MOUNTAIN = "Rocky Mountains"

class LootTable:
    def __init__(self, id_, items):
        self.id = id_
        self.items = items
    
    def __repr__(self):
        desc = ""
        desc += f"<Table: {self.id}>\n"
        for k, v in self.items.items():
            desc += f"{k}: {v}\n"
        return desc

class StructureType(Enum):
    SETTLEMENT = "settlement"
    RUIN = "ruin"
    FORMATION = "formation"

class Structure:
    def __init__(self, name, loottable: LootTable, structure_type: StructureType):
        self.name = name
        self.loottable = loottable
        self.structure_type = structure_type

    def __repr__(self):
        return f"<{self.structure_type.value.title()}: {self.name}>"
    
    @staticmethod
    def load_table_from_json(file_path="gamedata/resources/loot tables/loot_tables.json"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No item file at {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            loot_tables = json.load(f)

        loaded_tables = {}
        for data in loot_tables:
            table = LootTable(
                id_=data["id"],
                #type_=data["type"],
                items=data["items"]
            )
            loaded_tables[data["id"]] = table

        return loaded_tables
    
LOOT_TABLES = Structure.load_table_from_json()
print(f"Loot tables: {LOOT_TABLES}")

PLACEHOLDER_STRUCTURES = [
    "Ancient Ruins", "Abandoned Hut", "Watchtower",
    "Cave Entrance", "Forest Shrine", "Trading Post",
    "Mysterious Statue", "Burial Site", "Old Campfire"
]

class Tile:
    def __init__(self, x, y, biome, altitude, seed=0):
        self.x = x
        self.y = y
        self.seed = seed
        self.biome = biome
        self.altitude = altitude
        self.structures = self._generate_structures()
        self.entities = []

    def describe(self):
        desc = f"Tile ({self.x}, {self.y}) - {self.biome.value}, Altitude: {self.altitude}"
        if self.structures:
            desc += f"\nStructures:" 
            for s in self.structures:
                desc += f"\n{s.name}"
                desc += debug(f"\n{s.loottable}")
        return desc

    """
    @staticmethod
    def _generate_structures():
        num_structures = random.choices([0, 1, 2, 3], weights=[15, 60, 20, 5])[0]
        return [
            Structure(
                name=random.choice(PLACEHOLDER_STRUCTURES),
                loottable=random.choice(list(LOOT_TABLES.values()))
            )
            for _ in range(num_structures)
        ]
    """
    def _generate_structures(self):
        tile_seed = f"{self.x},{self.y},{self.seed}"
        rng = random.Random(tile_seed)

        structures = []
        num_structures = rng.choices([4, 2, 3, 5], weights=[15, 60, 20, 5])[0]
        for _ in range(num_structures):
            structures.append(
                Structure(
                    name=rng.choice(PLACEHOLDER_STRUCTURES),
                    loottable=rng.choice(list(LOOT_TABLES.values())),
                    structure_type=rng.choice(list(StructureType))
                )
            )
        return structures

class World:
    def __init__(self, name, seed, width=50, height=50, worldType=WorldTypes.NORMAL):
        self.name = name
        self.seed = seed
        self.worldType = worldType
        self.time = GameTime()

        self.width = width
        self.height = height
        self.tiles = WorldGenerator.generate(width, height, WorldTypes.NORMAL, seed)
    
    def get_tile(self, x, y=None):
        if type(x) == tuple:
            return self.tiles.get((x[0], x[1]))

        return self.tiles.get((x, y))
    
    def get_center_tile(self):
        all_coords = self.tiles.keys()
        xs = [x for x, _ in all_coords]
        ys = [y for _, y in all_coords]
        center_x = int((min(xs) + max(xs)) // 2)
        center_y = int((min(ys) + max(ys)) // 2)
        return (center_x, center_y)

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
    
    def print_altitude_map(self, display_width=50):
        print("\n")
        step_x = max(1, self.width // display_width)
        step_y = max(1, self.height // display_width)

        for y in range(0, self.height, step_y):
            row = ""
            for x in range(0, self.width, step_x):
                tile = self.get_tile(x, y)
                if tile:
                    color = gradient_shade(tile.altitude)
                    row += f"{color}{tile.altitude}{RESET}"
                else:
                    row += "?"
            print(row)
        return "\n"

class WorldGenerator:
    @classmethod
    def generate(cls, width, height, worldType, seed):
        if worldType == WorldTypes.NORMAL:
            return cls._generate_normal_world(width, height, seed)
    
    @classmethod
    def _generate_normal_world(cls, width, height, seed):
        worldTiles = {}
        print(debug(f"seed={seed}, type={type(seed)}"))
        for x in range(width):
            for y in range(height):
                biome = random.choice(list(Biome))
                altitude = cls._get_altitude(x, y, seed)
                tile = Tile(x, y, biome, altitude, seed)
                worldTiles[(x, y)] = tile
        
        return worldTiles
    
    @staticmethod
    def _get_altitude(x, y, seed=0):
        return get_altitude(x, y, seed)
