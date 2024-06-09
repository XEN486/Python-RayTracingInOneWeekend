from rtweekend import *
from vector import *
from ray import *
from color import *
from texture import *
import math

class material:
    def __init__(self): ...

    def emitted(self, u, v, p):
        return color(0,0,0)
    
    def scatter(self, r_in, rec, attenuation, scattered):
        return False, rec, attenuation, scattered

class lambertian(material):
    def __init__(self, albedo):
        if type(albedo) == color:
            self.tex = solid_color(albedo)
        else:
            self.tex = albedo

    def scatter(self, r_in, rec, attenuation, scattered):
        scatter_direction = rec.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = rec.normal
        
        scattered = ray(rec.p, scatter_direction, r_in.time)
        attenuation = self.tex.value(rec.u, rec.v, rec.p)
        return True, rec, attenuation, scattered

class metal(material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = fuzz
        
    def scatter(self, r_in, rec, attenuation, scattered):
        reflected = reflect(r_in.direction, rec.normal)
        reflected = unit_vector(reflected) + (random_unit_vector() * self.fuzz)
        scattered = ray(rec.p, reflected, r_in.time)
        attenuation = self.albedo
        return (dot(scattered.direction, rec.normal) > 0), rec, attenuation, scattered

class dielectric(material):
    def __init__(self, refraction_index):
        self.refraction_index = refraction_index

    def scatter(self, r_in, rec, attenuation, scattered):
        attenuation = color(1.0, 1.0, 1.0)
        ri = (1.0 / self.refraction_index) if rec.front_face else self.refraction_index

        unit_direction = unit_vector(r_in.direction)
        cos_theta = min(dot(vec3(-unit_direction[0], -unit_direction[1], -unit_direction[2]), rec.normal), 1) # maybe add a neg function?
        sin_theta = math.sqrt(1 - cos_theta*cos_theta)

        cannot_refract = ri * sin_theta > 1.0

        # reflect if we cannot refract
        direction = reflect(unit_direction, rec.normal) if cannot_refract or self._reflectance(cos_theta, ri) > random_double() else refract(unit_direction, rec.normal, ri)

        scattered = ray(rec.p, direction, r_in.time)
        return True, rec, attenuation, scattered

    def _reflectance(self, cosine, refraction_index):
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1 - r0) * pow((1 - cosine), 5)

class diffuse_light(material):
    def __init__(self, emit):
        if type(emit) == color:
            self.tex = solid_color(emit)
        else:
            self.tex = emit

    def emitted(self, u, v, p):
        return self.tex.value(u, v, p)
