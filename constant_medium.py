from rtweekend import *
from hittable import *
from material import *
from texture import *

import math

class constant_medium(hittable):
    def __init__(self, boundary, density, tex_or_albedo):
        self.boundary = boundary
        self.neg_inv_density = -1 / density
        self.phase_function = isotropic(tex_or_albedo)
        self.bounding_box = boundary.bounding_box

    def hit(self, r, ray_t, rec):
        enableDebug = False
        debugging = enableDebug and random_double() < 0.00001

        rec1 = hit_record(None,None,None,None)
        rec2 = hit_record(None,None,None,None)

        ub_hit, rec1 = self.boundary.hit(r, universe_i, rec1)
        if not ub_hit:
            return False, rec

        ut_hit, rec2 = self.boundary.hit(r, interval(rec1.t+0.0001, infinity), rec2)
        if not ut_hit:
            return False, rec

        if debugging: sys.stdout.write(f'\nnt_min={rec1.t}, t_max={rec2.t}')

        if (rec1.t < ray_t.min): rec1.t = ray_t.min
        if (rec2.t > ray_t.max): rec2.t = ray_t.max

        if (rec1.t >= rec2.t):
            return False, rec

        if (rec1.t < 0):
            rec1.t = 0

        ray_length = r.direction.length
        distance_inside_boundary = (rec2.t - rec1.t) * ray_length
        hit_distance = self.neg_inv_density * math.log(random_double())

        if hit_distance > distance_inside_boundary:
            return False, rec

        rec.t = rec1.t + hit_distance / ray_length
        rec.p = r.at(rec.t)

        if debugging:
            sys.stdout.write(f'hit_distance = {hit_distance}\nrec.t = {rec.t}\nrec.p = {rec.p}\n')

        rec.normal = vec3(1,0,0)
        rec.front_face = True
        rec.mat = self.phase_function

        return True, rec
