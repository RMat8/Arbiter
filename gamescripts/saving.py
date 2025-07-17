#gamescrips/gamesavesystem.py
import os
import shutil
import pickle
import configparser
from datetime import datetime

#modules
from .game_state_manager import GameStateManager
from .colors import *

class GameSaveSystem():
    SAVE_DIRECTORY = "gamedata\saves"
    os.makedirs(SAVE_DIRECTORY, exist_ok=True)
    CURRENT_SAVE = None

    @staticmethod
    def new_game(game_state, slot_name=None):
        if slot_name is None:
            slot_name = input("Please enter a name for the save> ")

        save_path = os.path.join(GameSaveSystem.SAVE_DIRECTORY, slot_name)

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        save_game_state_path = os.path.join(save_path, "game_state.pkl")
        save_config_path = os.path.join(save_path, "config.ini")

        try:
            with open(save_game_state_path, "wb") as save_file:
                pickle.dump(game_state, save_file)

            with open(save_config_path, "w") as save_config:
                config = configparser.ConfigParser()

                config["gameSettings"] = {
                    "difficulty": "normal",
                    "startingWorldType": "normal"
                }
                
                config.write(save_config)

            GameSaveSystem.CURRENT_SAVE = slot_name
            GameStateManager.set(game_state)
            print(f"Game created successfully at {save_path}")
            return True
        except Exception as e:
            GameSaveSystem.CURRENT_SAVE = None
            print(f"Error creating game: {e}")
            return False
        
    @staticmethod
    def save_progress(game_state, slot_name):
        save_path = os.path.join(GameSaveSystem.SAVE_DIRECTORY, slot_name)
        save_game_state_path = os.path.join(save_path, "game_state.pkl")

        if not os.path.exists(save_path):
            GameSaveSystem.new_game(game_state, slot_name)

        try:
            with open(save_game_state_path, "wb") as save_file:
                pickle.dump(game_state, save_file)
            print(f"Progress saved to {save_game_state_path}")
            return True
        except Exception as e:
            print(f"Error saving progress: {e}")
            return False

    @staticmethod
    def load_game(slot_name):
        save_path = os.path.join(GameSaveSystem.SAVE_DIRECTORY, slot_name)

        save_file_path = os.path.join(save_path, "game_state.pkl")

        try:
            if not os.path.exists(save_path):
                print(f"No save found at {save_path}")
                return None
            
            with open(save_file_path, "rb") as save_file:
                game_state = pickle.load(save_file)
            
            GameSaveSystem.CURRENT_SAVE = slot_name
            GameStateManager.set(game_state)
            print(f"Game loaded successfully from {save_path}")
            return game_state
        except Exception as e:
            GameSaveSystem.CURRENT_SAVE = None
            return f"Error loading game: {e}"
    
    @staticmethod
    def list_saves():
        saves = []
        for save in os.listdir(GameSaveSystem.SAVE_DIRECTORY):
            if os.path.isdir(os.path.join(GameSaveSystem.SAVE_DIRECTORY, save)):
                saves.append(save)
        return saves
    
    @staticmethod
    def delete_save(slot_name):
        save_path = os.path.join(GameSaveSystem.SAVE_DIRECTORY, slot_name)
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
            print(f"Save '{BRIGHT_PURPLE}{BOLD}{slot_name}{RESET}' deleted successfully.")
        else:
            print(f"No save file found named '{slot_name}'.")
