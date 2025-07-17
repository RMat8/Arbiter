#game/noise.py
import math
from .colors import *

def lerp(a, b, t):
    return a + t * (b - a)

def fade(t):
    return t * t * (3 - 2 * t)

def gradient_noise(x, y, seed=0, scale=0.005): #scale=0.1
    seed = int(seed)
    x *= scale
    y *= scale
    x0 = int(x)
    y0 = int(y)
    x1 = x0 + 1
    y1 = y0 + 1

    def random_value(ix, iy):
        r = math.sin(ix * 374761393 + iy * 668265263 + seed * 982451653) * 43758.5453
        return r - math.floor(r)
    
    v00 = random_value(x0, y0)
    v10 = random_value(x1, y0)
    v01 = random_value(x0, y1)
    v11 = random_value(x1, y1)

    fx = fade(x - x0)
    fy = fade(y - y0)

    # Interpolate along x
    i1 = lerp(v00, v10, fx)
    i2 = lerp(v01, v11, fx)

    # Interpolate along y
    final = lerp(i1, i2, fy)

    return final

def layered_noise(x, y, seed=0, scale=0.02, octaves=8, persistence=0.7): #scale=0.05 persistence=0.5
    total = 0
    amplitude = 12 #1
    max_amplitude = 0

    for i in range(octaves):
        val = gradient_noise(x, y, seed=seed + i, scale=scale)
        total += val * amplitude
        max_amplitude += amplitude
        amplitude *= persistence
        scale *= 2

    return total / max_amplitude  # Normalize to [0, 1]
