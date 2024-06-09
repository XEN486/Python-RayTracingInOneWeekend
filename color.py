from interval import *
from vector import *
import math

color = vec3

def linear_to_gamma(linear_component):
    if linear_component > 0:
        return math.sqrt(linear_component)

    return 0

def write_color(f, pixel_color):
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    r = linear_to_gamma(r)
    g = linear_to_gamma(g)
    b = linear_to_gamma(b)
    
    intensity = interval(0.000, 0.999)
    ir = int(256 * intensity.clamp(r))
    ig = int(256 * intensity.clamp(g))
    ib = int(256 * intensity.clamp(b))

    f.write(f'{ir} {ig} {ib}\n')
