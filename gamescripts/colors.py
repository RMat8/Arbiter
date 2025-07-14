#game/color.py

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BLACK = "\033[30m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BRIGHT_BLUE = "\033[38;2;0;150;255m"
DARK_BLUE = "\033[38;2;0;0;80m"
DARK_GREY  = "\033[90m"
GREY       = "\033[37m"
LIGHT_GREY = "\033[97m"
PURPLE      = "\033[35m"
BRIGHT_PURPLE = "\033[95m"

ITALIC = "\033[3m"
BOLD = "\033[1m"
RESET = "\033[0m"

def blue_shade(altitude):
    """
    Returns an ANSI escape code for a blue color shade based on altitude.
    Higher altitude = lighter blue.
    """
    altitude = max(0, min(100, altitude))

    red   = int((altitude / 100) * 40)
    green = int((altitude / 100) * 180)
    blue  = int(50 + (altitude / 100) * 220)

    return f"\033[38;2;{red};{green};{blue}m"

def debug(text):
    return f"{YELLOW}{text}{RESET}"
