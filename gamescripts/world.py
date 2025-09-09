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
    return int(val * 100) + 19 #offset to be 19 degrees higher

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

class Structure:
    def __init__(self, name, loottable: dict):
        self.name = name
        self.loottable = loottable

    def __repr__(self):
        return f"<{self.name}>"
    
    @staticmethod
    def load_tables_from_json(file_path="gamedata/resources/loot tables/loot_tables.json"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No item file at {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            loot_tables = json.load(f)

        loaded_tables = {}
        for data in loot_tables:
            id_=data["id"]
            items = data["items"]
            table = LootTable(id_=id_, items=items)
            loaded_tables[data["id"]] = table

        return loaded_tables
    
LOOT_TABLES = Structure.load_tables_from_json()
print(f"Loot tables: {LOOT_TABLES}")

def load_structures_from_json(file_path="gamedata/resources/structures/structures.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No structure file at {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        structures_data = json.load(f)


    loaded_structures = {}
    print(f"structures_data: {structures_data}")
    for struct_id, struct_info in structures_data.items():
        containers = struct_info.get("containers", {})

        container_objects = {
            name: LOOT_TABLES[loottable_id]
            for name, loottable_id in containers.items()
            if loottable_id in LOOT_TABLES
        }

        debug(f"Loaded structure '{struct_id}' with containers: {container_objects}")
        loaded_structures[struct_id] = Structure(
            name=struct_id,
            loottable=container_objects
        )

    return loaded_structures


STRUCTURES = load_structures_from_json()

class Tile:
    def __init__(self, x, y, biome, altitude, seed=0):
        self.x = x
        self.y = y
        self.seed = seed
        self.biome = biome
        self.altitude = altitude
        self.structures = self._generate_structures()
        self.entities = []

    def describe(self, expanded=False):
        desc = f"Tile ({self.x}, {self.y}) - {self.biome.value}, Altitude: {self.altitude}"
        desc += f"\nStructures:" 
        for s in self.structures:
            desc += f"\n- {s.name}"
            if expanded:
                for container, table in s.loottable.items():
                    desc += f"\n  {container}: {table.id}"
                    for item, weight in table.items.items():
                        desc += f"\n    {item}: {weight}"
                desc += "\n"
            else:
                for container, table in s.loottable.items():
                    desc += f"\n {container}: {table.id} ({len(table.items)} items)\n"

        return desc

    def _generate_structures(self):
        tile_seed = f"{self.x},{self.y},{self.seed}"
        rng = random.Random(tile_seed)

        structures = []
        num_structures = rng.choices([1, 2, 3, 4], weights=[15, 60, 20, 5])[0]
        for _ in range(num_structures):
            structure_name = rng.choice(list(STRUCTURES.keys()))
            structure_template = STRUCTURES[structure_name]
            
            loottable_copy = dict(structure_template.loottable)

            structures.append(
                Structure(
                    name=structure_template.name,
                    loottable=loottable_copy,
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
        self.tiles = WorldGenerator.generate(self.width, self.height, self.worldType, self.seed)
        
    
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
            return cls._generate_normal_world(width, height, worldType, seed)
    
    @classmethod
    def _generate_normal_world(cls, width, height, worldType, seed):
        worldTiles = {}
        rng = random.Random(seed)
        print(debug(f"seed={seed}, type={worldType}"))
        for x in range(width):
            for y in range(height):
                biome = rng.choice(list(Biome))
                altitude = cls._get_altitude(x, y, seed)
                tile = Tile(x, y, biome, altitude, seed)
                worldTiles[(x, y)] = tile
        
        return worldTiles
    
    @staticmethod
    def _get_altitude(x, y, seed=0):
        return get_altitude(x, y, seed)
