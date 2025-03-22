#gamescrips/gamesavesystem.py
import os
import pickle
from datetime import datetime

class GameSaveSystem():
    SAVE_DIRECTORY = "gamedata/saves"

    @staticmethod
    def _ensure_save_directory_exists():
        if not os.path.exists(GameSaveSystem.SAVE_DIRECTORY):
            os.makedirs(GameSaveSystem.SAVE_DIRECTORY)

    @staticmethod
    def save_game(game_state, slot_name=None):
        if slot_name is None:
            slot_name = f"save_{datetime.now().strftime("%Y%m#d_%H%M%S")}"
        else:
            slot_name = f"{slot_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}"
        
        if not slot_name.endswith(".pkl"):
            slot_name += ".pkl"
        
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
            if not os.path.exists(save_file_path):
                print(f"No save file found at {save_path}")
                return None
            
            with open(save_file_path, "rb") as save_file:
                game_state = pickle.load(save_file)
            print(f"Game loaded successfully from {save_file_path}")
            return game_state
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    @staticmethod
    def list_saves():
        save_directories = []
        for directory in os.listdir(GameSaveSystem.SAVE_DIRECTORY):
            if os.path.isdir(os.path.join(GameSaveSystem.SAVE_DIRECTORY, directory)):
                save_directories.append()
        return save_directories
    
    @staticmethod
    def delete_save(slot_name):
        save_path = os.path.join(GameSaveSystem.SAVE_DIRECTORY, slot_name)
        if os.path.exists(save_path):
            os.rmdir(save_path)
            print(f"Save '{slot_name}' deleted successfully.")
        else:
            print(f"No save file found named '{slot_name}'.")
