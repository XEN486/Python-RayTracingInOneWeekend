from rtweekend import *
from color import *
from interval import *
from perlin import *
from rtw_stb_image import rtw_image
import math

def clamp(x, min_value, max_value):
    return max(min(x, max_value), min_value)

class texture:
    def __init__(self, u, v, p): ...

class solid_color(texture):
    def __init__(self, albedo, green=None, blue=None):
        if green == None:
            self.albedo = albedo
        else:
            self.albedo = color(albedo, green, blue)

    def value(self, u, v, p):
        return self.albedo

class checker_texture(texture):
    def __init__(self, scale, c1_even, c2_odd):
        self.inv_scale = 1.0 / scale
        
        if type(c1_even) == texture:
            self.even = c1_even
            self.odd = c2_odd
        else:
            self.even = solid_color(c1_even)
            self.odd = solid_color(c2_odd)

    def value(self, u, v, p):
        xi = int(math.floor(self.inv_scale * p.x))
        yi = int(math.floor(self.inv_scale * p.y))
        zi = int(math.floor(self.inv_scale * p.z))

        isEven = (xi + yi + zi) % 2 == 0

        return self.even.value(u, v, p) if isEven else self.odd.value(u, v, p)

class image_texture(texture):
    def __init__(self, filename):
        self.image = rtw_image(filename)

    def value(self, u, v, p):
        if self.image.height() <= 0:
            return color(0, 1, 1)

        u = clamp(u, 0, 1)
        v = clamp(v, 0, 1)

        i = int(u * (self.image.width() - 1))
        j = int((1 - v) * (self.image.height() - 1))
        pixel = self.image.pixel_data(i, j)

        color_scale = 1.0 / 255.0
        return color(color_scale * pixel[0], color_scale * pixel[1], color_scale * pixel[2])

class noise_texture(texture):
    def __init__(self, scale=1):
        self.scale = scale
        self.noise = perlin()

    def value(self, u, v, p):
        #return color(1,1,1) * 0.5 * (1.0 + self.noise.noise(p * self.scale))
        return color(.5,.5,.5) * (1+math.sin(self.scale * p.z + 10 * self.noise.turb(p, 7)))
