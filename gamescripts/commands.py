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
def help_command():
    output = "\n"
    output += "Available commands: \n"
    for command, description in MENU_COMMAND_DESCRIPTIONS.items():
        output += f"{command}: {description}\n"
    return output

def save_command(arg):
    save_system = GameSaveSystem()
    save_system.save_game(arg)
    return save_system

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

def delete_save_command(filename):
    save_system = GameSaveSystem()
    save_system.delete_save(filename)

def list_saves_command():
    save_system = GameSaveSystem()
    save_files = save_system.list_saves()
    if save_files:
        print("Available saves:")
        for save_file in save_files:
            print(f"- {save_file}")
    else:
        print("No save files found")

def create_new_game(saveName):
    # Introduce
    print("Welcome")
    time.sleep(0.1)
    name = input("Write your name> ")
    playerEntity = Player(name)
    print(f"Hello, {name}, Your journey begins here.")
    time.sleep(0.1)
    print("Type 'help' to learn more...\n")
    
    # Config
    config = configparser.ConfigParser()
    config.read("gamedata/config.ini")
    difficulty = config["gameSettings"]["difficulty"]
    startingWorldType = config["gameSettings"]["startingWorldType"]

    # Initialize game state
    game_state = {
        "name": saveName,
        "worldType": startingWorldType,
        "player": { #to be revised
            "name": name,
            "position": (0, 0)  # Assuming starting position is (0, 0)
        }
    }

    # Save the new game state
    save_system = GameSaveSystem()
    save_system.save_game(game_state)

    # Start the main game loop
    return True

def new_game_command(arg=None):
    if not arg:
        arg = input("Enter the name of the save> ")

    create_new_game(arg)
    return "New game created and started."

def exit_command(arg=None):
    print("Exiting the game. Goodbye!")
    sys.exit()

MENU_COMMANDS = {
    "help": help_command,
    "save": save_command,
    "load": load_command,
    "new": new_game_command,
    "delete": delete_save_command,
    "list": list_saves_command,
    "exit": exit_command
}

MENU_COMMAND_DESCRIPTIONS ={
    "help": "Displays a list of available commands.",
    "save (file)": "Saves the current game state.",
    "load (file)": "Loads a saved game state.",
    "new (file)": "Creates a new game",
    "delete (file)": "Deletes a saved game.",
    "list": "Lists all saved game slots.",
    "exit": "Exits the game."
}

#ingame command functions

def game_help():
    output = "\n"
    output += "Available actions: \n"
    for command, description in GAME_COMMAND_DESCRIPTIONS.items():
        output += f"{command}: {description}\n"
    return output

def quit_game():
    return "Exiting the saved game"

GAME_COMMANDS = {
    "help": game_help,
    "quit": quit_game
}

GAME_COMMAND_DESCRIPTIONS ={
    "help": "Displays a list of available actions.",
    "quit": "Exits the saved game."
}
