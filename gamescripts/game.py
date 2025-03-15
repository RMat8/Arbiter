#game/game.py
import json
import configparser
import os
from datetime import datetime

#modules
from .player import Player
from .world import World, WorldTypes

class GameSaveSystem():
    def __init__(self, save_directory="gamedata/saves"):
        self.save_directory = save_directory
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
    
    def save_game(self, game_state, slot_name=None):
        if slot_name is None:
            slot_name = f"save_{datetime.now().strftime("%Y%m#d_%H%M%S")}"
        
        if not slot_name.endswith(".json"):
            slot_name += ".json"
        
        save_path = os.path.join(self.save_directory, slot_name)

        try:
            with open(save_path, "w") as save_file:
                json.dump(game_state, save_file, indent=4)
            print(f"Game saved successfully to {save_path}")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, slot_name):
        if not slot_name.endswith(".json"):
            slot_name += ".json"
        
        save_path = os.path.join(self.save_directory, slot_name)

        try:
            if not os.path.exists(save_path):
                print(f"No save file found at {save_path}")
                return None
            
            with open(save_path, "r") as save_file:
                game_state = json.load(save_file)
            print(f"Game loaded successfully from {save_path}")
            return game_state
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

def game_init(arg=0):
    if arg == 0:
        #introduce
        print("Welcome")
        name = input("Write your name> ")
        playerEntity = Player(name)
        print(f"Hello, {name}, Your journey begins here.")
        print("Type 'help' to learn more...")
        
        #config
        config = configparser.ConfigParser()
        config.read("Python-Text-Adventure-Game/gamedata/config.ini")
        difficulty = config["gameSettings"]["difficulty"]
        startingWorldType = config["gameSettings"]["startingWorldType"]

        #initialize
        main(difficulty)
    else:
        pass

def parse_input(userInput):
    parts = userInput.lower().strip().split(maxsplit=1)
    return parts[0], parts[1] if len(parts) > 1 else ""

def main(difficulty):
    state = "menu"
    while state != "exit":
        uInput = parse_input(input("What do you want to do? "))
        print(uInput)
