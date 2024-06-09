import math
import random

infinity = float('inf')
pi = math.pi

def degrees_to_radians(degrees):
    return degrees * pi / 180

def random_double(min=0, max=1):
    return random.uniform(min, max)

def random_int(min, max):
    return random.randint(min, max)
