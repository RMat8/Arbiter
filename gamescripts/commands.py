#gamescripts/commands.py
import os
import sys
import time
import configparser
import random

#modules
from .colors import *
from .saving import GameSaveSystem
from .game_state_manager import GameStateManager
from .player import Player
from .world import World, HostilityLevel, Biome
from .item import ITEMS

#menu command functions
class MenuCommands:
    @staticmethod
    def help_command():
        output = "\n"
        output += f"{BRIGHT_PURPLE}Available commands: {RESET}\n"
        for command, description in COMMANDS["MENU"]["DESCRIPTIONS"].items():
            output += f"{command}: {description}\n"
        return output

    @staticmethod
    def load_command(arg=None):
        save_system = GameSaveSystem()
        if not arg:
            print("Please specify save to load from directory")
            save_files = save_system.list_saves()
            if save_files:
                for save_file in save_files:
                    print(f"- {save_file}")
                arg = input("Please specify the save to load: ")
            else:
                return "No save files found"
        else:
            try:
                save = save_system.load_game(arg)
                game_state = GameStateManager.get()
            except Exception as e:
                return f"Error loading game: {e}"

        """
        current_world = GameStateManager.get()["player_location"]["current_world"]
        current_world.print_altitude_map()
        """
        return (f"Save succesfully loaded\nWelcome back, {game_state["player"].name}", game_state, "game")

    @staticmethod
    def delete_save_command(filename, confirmation=None):
        if not confirmation == "Y":
            confirmation = input("Are you sure? Type Y/N> ")
        
        if confirmation == "Y":
            save_system = GameSaveSystem()
            if filename == "*":
                for save in save_system.list_saves():
                    save_system.delete_save(save)
            else:
                save_system.delete_save(filename)

        return ""

    @staticmethod
    def list_saves_command():
        save_system = GameSaveSystem()
        save_files = save_system.list_saves()
        if save_files:
            output = "Available saves:\n"
            for save_file in save_files:
                output += f"- {save_file}\n"
        else:
            output = "No save files found"
        
        return output

    @staticmethod
    def create_new_game(save_name, player_name, seed): #this is the black box of the new_game_command
        # Introduce
        playerEntity = Player(f"{CYAN}{player_name}{RESET}")
        initialWorld = World(save_name, seed)

        """ #display tile data
        print(f"World: {initialWorld.name}")
        print(f"Tile count: {len(initialWorld.tiles)}")
        for coords, tile in initialWorld.tiles.items():
            print(f"{coords}: {tile.describe()}")
        """

        """#display tile noise altitude
        initialWorld.print_altitude_map()
        """

        print(f"Hello, {player_name}, Your journey begins here.")
        time.sleep(0.1)
        print("Type 'help' to learn more...\n")
        
        """        # Config
        config = configparser.ConfigParser()
        config.read("gamedata/config.ini")
        difficulty = config["gameSettings"]["difficulty"]
        startingWorldType = config["gameSettings"]["startingWorldType"]"""

        # Initialize game state
        """        game_state = {
            "name": saveName,
            "worldType": startingWorldType,
            "player": { #to be revised
                "name": name,
                "position": (0, 0)  # Assuming starting position is (0, 0)
            }
        }"""

        game_state = {
            "worlds": [initialWorld],
            "player": playerEntity,
            "player_location": {
                "current_world": initialWorld,
                "current_region": None,
                "player_position": (0, 0),
                "current_tile": initialWorld.get_tile(0, 0)
            }
        }

        if not initialWorld in game_state["worlds"]:
            game_state["worlds"].append(initialWorld)

        # Save the new game state
        save_system = GameSaveSystem()
        save_system.new_game(game_state, save_name)
        game_state = debug(f"{GameStateManager.get()}")
        print(game_state)

        # Start the main game loop
        return True, game_state

    @staticmethod
    def new_game_command(save_name=None, difficulty=None, player_name=None, seed=None): #this is the function that acts as the command
        if not save_name:
            save_name = input("Enter the name of the save> ")
        
        if not difficulty:
            print(f"{GREEN}DIFFICULTIES{RESET}\n")
            for n, v in HostilityLevel.__members__.items():
                print(f"{n}: {v.value}")

            difficulty = input("\nType a number to choose difficulty> ")

        if not player_name:
            player_name = input("Write your name> ")
        else:
            seed = int(seed)

        if not seed:
            seed = random.randint(0, 99999999)

        return ("\nNew game created and started.", MenuCommands.create_new_game(save_name, player_name, seed)[1], "game")
    
    @staticmethod
    def exit_command(arg=None):
        print("Exiting the game. Goodbye!")
        sys.exit()

#ingame command functions
class GameCommands():
    @staticmethod
    def master_info(): #both implicitly and explicitly called
        output = f"INFO PLACEHOLDER\n"
        output += debug(f"{Biome.ICECAP}")
        return output

    @staticmethod
    def game_help():
        output = "\n"
        output += f"{BRIGHT_PURPLE}Available actions: {RESET}\n"
        for command, description in COMMANDS["GAME"]["DESCRIPTIONS"].items():
            output += f"{command}: {description}\n"
        
        output += f"\nGame State:\n"
        output += f"{GameStateManager.get()}"
        return debug(output)
        
    @staticmethod
    def save_command(game_state=None, name=None):
        save_system = GameSaveSystem()

        if not game_state:
            game_state = GameStateManager.get()

        if not name:
            name = GameSaveSystem.CURRENT_SAVE

        save_system.save_progress(game_state, name)
        return f"Game succesfully saved as {name}"
    
    @staticmethod
    def world_map():
        current_world = GameStateManager.get()["player_location"]["current_world"]
        current_world.print_altitude_map()
        return ""

    @staticmethod
    def region_map():
        current_tile = GameStateManager.get()["player_location"]["current_tile"]
        return current_tile.describe()
    
    @staticmethod
    def catalogue():
        for k, _v in ITEMS.items():
            print(f"{k.name}: {k.description}")
            print(f"Attributes: {k.attributes}")
        return ""

    @staticmethod
    def quit_game(game_exit=None):
        if not game_exit == "exit":
            GameStateManager.reset()
            return ("Exiting the saved game\n", "menu", "menu") #second value is a placeholder for what would normally be a huge game_state object
        else:
            GameStateManager.reset()
            MenuCommands.exit_command()

COMMANDS = {
    "MENU": {
        "COMMANDS": {
            "help": MenuCommands.help_command,
            "load": MenuCommands.load_command,
            "new": MenuCommands.new_game_command,
            "delete": MenuCommands.delete_save_command,
            "list": MenuCommands.list_saves_command,
            "exit": MenuCommands.exit_command
        },
       "DESCRIPTIONS": {
            "help": "Displays a list of available commands.",
            "load (save)": "Loads a saved game.",
            "new (save)": "Creates a new game.",
            "delete (save)": "Deletes a saved game.",
            "list": "Lists all saved games.",
            "exit": "Exits the game."
        }
    },
    "GAME": {
        "COMMANDS": {
            "info": GameCommands.master_info,
            "help": GameCommands.game_help,
            "save (save name; optional)": GameCommands.save_command,
            "map": GameCommands.world_map,
            "region": GameCommands.region_map,
            "catalogue": GameCommands.catalogue,
            "quit": GameCommands.quit_game
        },
        "DESCRIPTIONS" : {
            "info": "Shows general info about your current surroundings and situation.",
            "help": "Displays a list of available actions.",
            "save (name)": "Saves the current game state as specified save name (leave blank to overwrite current save).",
            "map": "Displays an altitude map of the known tiles.",
            "region": "Displays a map of the current tile.",
            "quit": "Exits the saved game."
        }
    }
}
