#game/game.py
import json
import configparser

#modules
from .player import Player
from .world import World

def game_init(arg=0):
    if arg == 0:
        #introduce
        print("Welcome")
        name = input("Write your name> ")
        print(f"Hello, {name}, Your journey begins here...")
        
        #config
        config = configparser.ConfigParser()
        config.read("config.ini")
        difficulty = config["settings"]["difficulty"]

        #initialize
        main(difficulty)
    else:
        pass

def parse_input(user_input):
    parts = user_input.lower().strip().split(maxsplit=1)
    return parts[0], parts[1] if len(parts) > 1 else ""

def main():
    state = "menu"
    while state != "exit":
        if state == "menu":
            pass
        elif state == "ingame":
            pass
