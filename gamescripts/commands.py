#gamescripts/commands.py
import os
import sys
import time
import configparser

#modules
from .colors import *
from .saving import GameSaveSystem, GameStateManager
from .player import Player
from .world import World, WorldTypes

#menu command functions

class MenuCommands:
    @staticmethod
    def help_command():
        output = "\n"
        output += "Available commands: \n"
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

        return (f"Save succesfully loaded\nWelcome back, {CYAN}{game_state["player"].name}{RESET}", game_state, "game")

    @staticmethod
    def delete_save_command(filename):
        save_system = GameSaveSystem()
        save_system.delete_save(filename)

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
    def create_new_game(save_name): #this is the black box of the new_game_command
        # Introduce
        print("Welcome")
        time.sleep(0.1)
        name = input("Write your name> ")
        playerEntity = Player(name)
        initialWorld = World(name)
        print(f"Hello, {CYAN}{name}{RESET}, Your journey begins here.")
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
                "player_position": (0, 0)
            }
        }

        if not initialWorld in game_state["worlds"]:
            game_state["worlds"].append(initialWorld)

        # Save the new game state
        save_system = GameSaveSystem()
        save_system.new_game(game_state, save_name)
        game_state = GameStateManager.get()

        # Start the main game loop
        return True, game_state

    @staticmethod
    def new_game_command(arg): #this is the function that acts as the command
        if not arg:
            arg = input("Enter the name of the save> ")

        return ("New game created and started.", MenuCommands.create_new_game(arg)[1], "game")

    @staticmethod
    def exit_command(arg=None):
        print("Exiting the game. Goodbye!")
        sys.exit()


#ingame command functions
class GameCommands():
    @staticmethod
    def game_help():
        output = "\n"
        output += "Available actions: \n"
        for command, description in COMMANDS["GAME"]["DESCRIPTIONS"].items():
            output += f"{command}: {description}\n"
        
        output += "\nGame State:\n"
        output += f"{GameStateManager.get()}"
        return output
        
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
    def quit_game():
        GameStateManager.reset()
        return ("Exiting the saved game", "menu", "menu") #second value is a placeholder for what would normally be a huge game_state object

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
            "help": GameCommands.game_help,
            "save (save name; optional)": GameCommands.save_command,
            "quit": GameCommands.quit_game
        },
        "DESCRIPTIONS" : {
            "help": "Displays a list of available actions.",
            "save (name)": "Saves the current game state as specified save name (leave blank to overwrite current save).",
            "quit": "Exits the saved game."
        }
    }
}
