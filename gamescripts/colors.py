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

"""
def gradient_shade(altitude):

    #Returns an ANSI escape code for a blue color shade based on altitude.
    #Higher altitude = lighter blue.
 
    altitude = max(0, min(100, altitude))

    red   = int((altitude / 100) * 40) #int((altitude / 100) * 40)
    green = int(100 + (altitude / 95) * 220) #int((altitude / 100) * 180)
    blue  = int((altitude / 100) * 180) #int(50 + (altitude / 100) * 220)

    return f"\033[38;2;{red};{green};{blue}m"
"""

def gradient_shade(altitude):
    altitude = max(0, min(100, altitude))

    if altitude <= 30:
        # Blue gradient: Dark blue to lighter blue
        t = altitude / 30
        r = int(0 * (1 - t) + 5 * t) #+ 30
        g = int(0 * (1 - t) + 35 * t) #+ 60
        b = int(90 * (1 - t) + 180 * t) #+ 200
    
    elif altitude <= 70:
        # Green gradient: Blue/green → bright green
        t = (altitude - 30) / 40
        r = int(30 * (1 - t) + 50 * t)
        g = int(60 * (1 - t) + 220 * t)
        b = int(200 * (1 - t) + 80 * t)
    
    else:
        # White gradient: Green → white
        t = (altitude - 70) / 11
        r = int(50 * (1 - t) + 255 * t)
        g = int(220 * (1 - t) + 255 * t)
        b = int(80 * (1 - t) + 255 * t)

    return f"\033[38;2;{r};{g};{b}m"

def debug(text):
    return f"{YELLOW}{text}{RESET}"
