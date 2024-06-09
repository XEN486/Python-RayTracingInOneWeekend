# Code from Shiva Kannan
import math
from rtweekend import *

# Decorator for checking Vector3 types
# Used this piece of code :
# https://stackoverflow.com/questions/15299878/how-to-use-python-decorators-to-check-function-arguments
def accepts(*types):
    def check_accepts(f):
        assert len(types) == f.__code__.co_argcount

        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), \
                       "arg %r does not match %s" % (a, t)
            return f(*args, **kwds)
        new_f.__name__ = f.__name__
        return new_f
    return check_accepts


class Vector3(list):

    def __init__(self, e0, e1, e2):
        self.append(float(e0))
        self.append(float(e1))
        self.append(float(e2))
        # XYZ coordinates
        self.x = e0
        self.y = e1
        self.z = e2
        # RGB
        self.r = e0
        self.g = e1
        self.b = e2
        # Length
        self.length = math.sqrt(e0*e0 + e1*e1 + e2*e2)
        self.squared_length = (e0*e0 + e1*e1 + e2*e2)

    def __add__(self, other):
        return Vector3(self[0] + other[0],
                       self[1] + other[1],
                       self[2] + other[2])

    def __sub__(self, other):
        return Vector3(self[0] - other[0],
                       self[1] - other[1],
                       self[2] - other[2])

    def __mul__(self, other):
        return Vector3(self[0] * other,
                       self[1] * other,
                       self[2] * other)

    def mul(self, other):
        return Vector3(self[0] * other[0],
                       self[1] * other[1],
                       self[2] * other[2])

    def __truediv__(self, other):
        return Vector3(self[0] / other,
                       self[1] / other,
                       self[2] / other)

    def __neg__(self):
        return Vector3(-self[0], -self[1], -self[2])

    def make_unit_vector(self):
        """
        Makes the current vector it's unit vector
        :return:
        """
        self[0] = self[0]/self.length
        self[1] = self[1]/self.length
        self[2] = self[2]/self.length

    def near_zero(self):
        s = 1e-8
        return (abs(self[0]) < s) and (abs(self[1]) < s) and (abs(self[2]) < s)


@accepts(Vector3, Vector3)
def dot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]


@accepts(Vector3, Vector3)
def cross(v1, v2):
    return Vector3(v1[1]*v2[2] - v1[2]*v2[1],
                   v1[2]*v2[0] - v1[0]*v2[2],
                   v1[0]*v2[1] - v1[1]*v2[0])


@accepts(Vector3)
def unit_vector(vector):
    return Vector3(vector[0] / vector.length, vector[1] / vector.length, vector[2] / vector.length)

def random(min=0, max=1):
    r1 = random_double(min, max)
    r2 = random_double(min, max)
    r3 = random_double(min, max)
    return vec3(r1, r2, r3)

def random_in_unit_sphere():
    while True:
        p = random(-1, 1)
        if (p.squared_length < 1):
            return p

def random_unit_vector():
    return unit_vector(random_in_unit_sphere())

@accepts(Vector3)
def random_on_hemisphere(normal):
    on_unit_sphere = random_unit_vector()
    if (dot(on_unit_sphere, normal) > 0.0):
        return on_unit_sphere

    return Vector3(0 - normal[0], 0 - normal[1], 0 - normal[2])

# this is asinine
@accepts(Vector3, Vector3)
def reflect(v, n):
    d = 2 * dot(v, n)
    s = v - Vector3(d, d, d)
    return s.mul(n)

def refract(uv, n, etai_over_etat):
    neg_uv = Vector3(0 - uv[0], 0 - uv[1], 0 - uv[2])
    cos_theta = min(dot(neg_uv, n), 1)
    r_out_perp = (uv + n * cos_theta) * etai_over_etat
    r_out_parallel = n * -math.sqrt(abs(1.0 - r_out_perp.squared_length))
    return r_out_perp + r_out_parallel

def random_in_unit_disc():
    while True:
        p = vec3(random_double(-1, 1), random_double(-1, 1), 0)
        if (p.squared_length < 1):
            return p

# aliases
vec3 = Vector3
point3 = Vector3
