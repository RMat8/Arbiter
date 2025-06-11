#game/game.py
import time
import os

#modules
from .colors import *
from .commands import MenuCommands, GameCommands, COMMANDS
from .game_state_manager import GameStateManager

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
    chunks = userInput.strip().split(" -")
    parsed = []

    for i, chunk in enumerate(chunks):
        if not chunk:
            continue
        parts = chunk.strip().split()
        if not parts:
            continue
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        parsed.append((command, args))

    """
    parts = userInput.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args
    """
    return parsed

def check_command(command, command_list):
    output = []

    game_state = GameStateManager.get()

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
        command_blocks = parse_input(uInput)
 
        for i in command_blocks:
            command = i[0]
            args = i[1]

            command_output = check_command(command, commands)
            if not command_output[0]:
                continue
            
            try:
                result = commands[command](*args) if args else commands[command]()
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
        
            if isinstance(result, tuple):
                print(result[0])
                game_state = result[1]
                if len(result) > 2 and result[2] in possible_states:
                    state = result[2]
            else:
                print(result)

            if state in possible_states:
                commands = COMMANDS[state.upper()]["COMMANDS"]
