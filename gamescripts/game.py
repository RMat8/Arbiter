#game/game.py
import time
import os

#modules
from .colors import *
from .commands import MenuCommands, GameCommands, COMMANDS
from .saving import GameStateManager

art = """
 █████  ██████╗ ██████╗    ██╗  ████████╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗   ╚═╝  ╚══██╦══╝██╔════╝██╔══██╗
███████║██████╔╝██████╔╝   ██╗     ██║   █████╗  ██████╔╝
██╔══██║██╔══██╗██╔══██╗   ██║     ██║   ██╔══╝  ██╔══██╗
██║  ██║██║  ██║███████║   ██║     ██║   ███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝     ╚═╝   ╚══════╝╚═╝  ╚═╝
"""

def game_init():
    os.system("cls")
    # Start the game by creating a new game or loading an existing one
    print("\n")
    #time.sleep(2)
    print(f"{MAGENTA}{art}{RESET}")
    #time.sleep(2)
    print("Type 'new' to start a new game or 'load <file>' to load an existing game.")
    #time.sleep(0.3)
    print("Type help for more information")
    #time.sleep(0.3)
    print("Type exit to quit.")
    #time.sleep(0.1)
    main(difficulty="normal")

def parse_input(userInput):
    parts = userInput.lower().strip().split(maxsplit=1)
    return parts[0], parts[1] if len(parts) > 1 else ""

def check_command(command, command_list, state):
    output = []

    if command in command_list:
        output.append(True)
    else:
        print(f"Unknown command: {command}. Type 'help' for a list of commands.")
        output.append(False)
    
    if command in ["new", "load"] and command in command_list:
        output.append("game")
    elif command in ["quit"] and command in command_list:
        output.append("menu")
    
    return output

#gameloop
def main(difficulty):
    possible_states = ["menu", "game"]
    state = "menu"
    commands = COMMANDS["MENU"]["COMMANDS"]

    while state != "exit":
        time.sleep(0.1)
        uInput = input("\nWhat do you want to do? ")
        command, arg = parse_input(uInput)
        command_output = check_command(command, commands, state)
        if len(command_output) == 2:
            state = command_output[1]
        
        if command_output[0]:
            if len(arg) > 0:
                result = commands[command](arg)
            else:
                try: #try to run command without arguments
                    result = commands[command]()
                except Exception as e:
                    print(f"An error occurred: {e}")
            
            if type(result) == tuple:
                print(result[0])
                game_state = result[1]
                try:
                    state = result[2]
                except Exception as e:
                    print(f"Output error: {e}")

            else:
                print(result)

            if state in possible_states:
                commands = COMMANDS[state.upper()]["COMMANDS"]
