#game/game.py
import time

#modules
from .commands import *

def game_init():
    # Start the game by creating a new game or loading an existing one
    print("Type 'new' to start a new game or 'load <file>' to load an existing game.")
    time.sleep(0.1)
    print("Type help for more information")
    time.sleep(0.1)
    print("Type exit to quit.")
    time.sleep(0.1)
    main(difficulty="normal")

def parse_input(userInput):
    parts = userInput.lower().strip().split(maxsplit=1)
    return parts[0], parts[1] if len(parts) > 1 else ""

def check_command(command, command_list):
    if command in command_list:
        return True
    else:
        print(f"Unknown command: {command}. Type 'help' for a list of commands.")
        return False

#gameloop
def main(difficulty):
    state = "menu"
    commands = MENU_COMMANDS
    command_descriptions = MENU_COMMAND_DESCRIPTIONS
    while state != "exit":
        time.sleep(0.1)
        uInput = input("What do you want to do? ")
        command, arg = parse_input(uInput)
        if check_command(command, commands):
            if len(arg) > 0:
                print(commands[command])(arg)
            else:
                try: #try to run command without arguments
                    print(commands[command]())
                except Exception as e:
                    print(f"An error occurred: {e}")
            
            if command == "new" or command == "load":
                state = "game"
                commands = GAME_COMMANDS
                command_descriptions = GAME_COMMAND_DESCRIPTIONS
            elif command == "quit" and state == "game":
                state = "menu"
                commands = MENU_COMMANDS
                command_descriptions = MENU_COMMAND_DESCRIPTIONS
