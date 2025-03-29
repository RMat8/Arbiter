#gamescrips/gamesavesystem.py
import os
import pickle
from datetime import datetime

class GameSaveSystem():
    SAVE_DIRECTORY = "Python-Text-Adventure-Game/gamedata/saves"

    @staticmethod
    def save_game(game_state, slot_name=None):
        if slot_name is None:
            slot_name = input("Please enter a name for the save> ")

        save_path = os.path.join(GameSaveSystem.SAVE_DIRECTORY, slot_name)

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        save_file_path = os.path.join(save_path, "game_state.pkl")

        try:
            with open(save_file_path, "wb") as save_file:
                pickle.dump(game_state, save_file)
            print(f"Game saved successfully to {save_path}")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    @staticmethod
    def load_game(slot_name):
        if not slot_name.endswith(".pkl"):
            slot_name += ".pkl"
        
        save_path = os.path.join(GameSaveSystem.SAVE_DIRECTORY, slot_name)

        save_file_path = os.path.join(save_path, "game_state.pkl")

        try:
            if not os.path.exists(save_path):
                print(f"No save found at {save_path}")
                return None
            
            with open(save_file_path, "rb") as save_file:
                game_state = pickle.load(save_file)
            print(f"Game loaded successfully from {save_file_path}")
            return game_state
        except Exception as e:
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
            os.rmdir(save_path)
            print(f"Save '{slot_name}' deleted successfully.")
        else:
            print(f"No save file found named '{slot_name}'.")
