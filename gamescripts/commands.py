#gamescripts/commands.py
import os
import sys
import time
import configparser

#modules
from .saving import GameSaveSystem
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
    def save_command(arg):
        save_system = GameSaveSystem()
        save_system.save_game(arg)
        return save_system

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
                print("No save files found")
                return None
        else:
            try:
                game_state = save_system.load_game(arg)
                if game_state is not None:
                    state = game_state["state"]
                    world = World(game_state["worldType"])
                    playerEntity = Player(game_state["player"]["name"], game_state["player"]["position"])
            except Exception as e:
                print(f"Error loading game: {e}")
                return None

        return game_state

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
    def create_new_game(save_name):
        # Introduce
        print("Welcome")
        time.sleep(0.1)
        name = input("Write your name> ")
        playerEntity = Player(name)
        print(f"Hello, {name}, Your journey begins here.")
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

        game_state = 0

        # Save the new game state
        save_system = GameSaveSystem()
        save_system.save_game(game_state, save_name)

        # Start the main game loop
        return True

    @staticmethod
    def new_game_command(arg=None):
        if not arg:
            arg = input("Enter the name of the save> ")

        print("New game created and started.")
        MenuCommands.create_new_game(arg)

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
        for command, description in COMMANDS["GAME"].items():
            output += f"{command}: {description}\n"
        return output

    @staticmethod
    def quit_game():
        return "Exiting the saved game"

COMMANDS = {
    "MENU": {
        "COMMANDS": {
            "help": MenuCommands.help_command,
            "save": MenuCommands.save_command,
            "load": MenuCommands.load_command,
            "new": MenuCommands.new_game_command,
            "delete": MenuCommands.delete_save_command,
            "list": MenuCommands.list_saves_command,
            "exit": MenuCommands.exit_command
        },
       "DESCRIPTIONS": {
            "help": "Displays a list of available commands.",
            "save (file)": "Saves the current game state.",
            "load (file)": "Loads a saved game state.",
            "new (file)": "Creates a new game",
            "delete (file)": "Deletes a saved game.",
            "list": "Lists all saved game slots.",
            "exit": "Exits the game."
        }
    },
    "GAME": {
        "COMMANDS": {
            "help": GameCommands.game_help,
            "quit": GameCommands.quit_game
        },
        "DESCRIPTIONS" : {
            "help": "Displays a list of available actions.",
            "quit": "Exits the saved game."
        }
    }
}
