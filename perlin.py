from rtweekend import *
import math
from vector import *

class perlin:
    def __init__(self, scale=1, point_count=256):
        self.point_count = point_count
        
        self.randvec = [vec3(0,0,0)] * point_count
        for i in range(point_count):
            self.randvec[i] = unit_vector(random(-1,1))

        self.perm_x = self.perlin_generate_perm()
        self.perm_y = self.perlin_generate_perm()
        self.perm_z = self.perlin_generate_perm()

    def noise(self, p):
        u = p.x - math.floor(p.x)
        v = p.y - math.floor(p.y)
        w = p.z - math.floor(p.z)

        u = u*u*(3-2*u)
        v = v*v*(3-2*v)
        w = w*w*(3-2*w)

        i = int(math.floor(p.x))
        j = int(math.floor(p.y))
        k = int(math.floor(p.z))

        nilvec = vec3(0,0,0)
        c = [[[nilvec, nilvec], [nilvec, nilvec]], [[nilvec, nilvec], [nilvec, nilvec]]]

        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    c[di][dj][dk] = self.randvec[
                        self.perm_x[(i+di) & 255] ^
                        self.perm_y[(j+dj) & 255] ^
                        self.perm_z[(k+dk) & 255]
                    ]

        return self.perlin_interp(c, u, v, w)

    def turb(self, p, depth):
        accum = 0.0
        temp_p = p
        weight = 1.0

        for i in range(depth):
            accum += weight * self.noise(temp_p)
            weight *= 0.5
            temp_p *= 2

        return abs(accum)

    def perlin_generate_perm(self):
        p = [0] * self.point_count

        for i in range(self.point_count):
            p[i] = i

        p = self.permute(p, self.point_count)
        return p

    def permute(self, p, n):
        for i in range(n-1, 0, -1):
            target = random_int(0, i)
            tmp = p[i]
            p[i] = p[target]
            p[target] = tmp
        return p

    def perlin_interp(self, c, u, v, w):
        uu = u*u*(3-2*u)
        vv = v*v*(3-2*v)
        ww = w*w*(3-2*w)
        accum = 0.0

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    weight_v = vec3(u-i, v-j, w-k)
                    accum += (i*uu + (1-i)*(1-uu)) * \
                             (j*vv + (1-j)*(1-vv)) * \
                             (k*ww + (1-k)*(1-ww)) * \
                             dot(c[i][j][k], weight_v)

        return accum


p = perlin()
