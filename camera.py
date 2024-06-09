from rtweekend import *
from vector import *
from ray import *
from color import *
from interval import *
from hittable_list import *
from hittable import *
from sphere import *
import sys
import time
import math
from concurrent.futures import ProcessPoolExecutor, as_completed

class camera:
    def __init__(self, aspect_ratio=1.0, image_width=100, samples_per_pixel=10, max_depth=10, vfov=90, lookfrom=point3(0,0,0), lookat=point3(0,0,-1), vup=point3(0,1,0), defocus_angle=0, focus_dist=10):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
        self.max_depth = max_depth
        self.vfov = vfov
        self.lookfrom = lookfrom
        self.lookat = lookat
        self.vup = vup
        self.defocus_angle = defocus_angle
        self.focus_dist = focus_dist

        # private
        self.image_height = None
        self.pixel_samples_scale = None
        self.center = None
        self.pixel00_loc = None
        self.pixel_delta_u = None
        self.pixel_delta_v = None
        self.u = None
        self.v = None
        self.w = None
        self.defocus_disc_u = None
        self.defocus_disc_v = None
        self.background = None

    def render(self, world):
        self._initialize()

        start = time.time()

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self._render_row, j, world) for j in range(self.image_height)]
            row_results = [None] * self.image_height
            for future in as_completed(futures):
                j, row_colors = future.result()
                row_results[j] = row_colors
                sys.stdout.write(f'\rScanlines remaining: {self.image_height - j - 1} ')

        with open('image.ppm', 'w') as f:
            f.write(f'P3\n{self.image_width} {self.image_height}\n255\n')
            for row_colors in row_results:
                for pixel_color in row_colors:
                    write_color(f, pixel_color)

        sys.stdout.write(f'\rDone.                 \nTime: {int(time.time() - start)}s\n')

    def _render_row(self, j, world):
        row_colors = []
        for i in range(self.image_width):
            pixel_color = color(0, 0, 0)
            for sample in range(self.samples_per_pixel):
                r = self._get_ray(i, j)
                pixel_color = pixel_color + self._ray_color(r, self.max_depth, world)
            row_colors.append(pixel_color * self.pixel_samples_scale)
        return j, row_colors

    def _initialize(self):
        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = 1 if (self.image_height < 1) else self.image_height

        self.pixel_samples_scale = 1.0 / self.samples_per_pixel

        self.center = self.lookfrom

        theta = degrees_to_radians(self.vfov)
        h = math.tan(theta / 2)
        viewport_height = 2 * h * self.focus_dist
        viewport_width = viewport_height * (self.image_width / self.image_height)

        w = unit_vector(self.lookfrom - self.lookat)
        u = unit_vector(cross(self.vup, w))
        v = cross(w, u)

        self.w = w
        self.u = u
        self.v = v

        viewport_u = u * viewport_width
        viewport_v = vec3(-v[0], -v[1], -v[2]) * viewport_height

        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        viewport_upper_left = self.center - (w * self.focus_dist) - viewport_u / 2 - viewport_v / 2
        self.pixel00_loc = viewport_upper_left + (self.pixel_delta_u + self.pixel_delta_v) / 2

        defocus_radius = self.focus_dist * math.tan(degrees_to_radians(self.defocus_angle / 2))
        self.defocus_disc_u = u * defocus_radius
        self.defocus_disc_v = v * defocus_radius

    def _get_ray(self, i, j):
        offset = self._sample_square()
        pixel_sample = self.pixel00_loc + (self.pixel_delta_u * (i + offset.x)) + (self.pixel_delta_v * (j + offset.y))
        
        ray_origin = self.center if self.defocus_angle <= 0 else self._defocus_disc_sample()
        ray_direction = pixel_sample - ray_origin
        ray_time = random_double()

        return ray(ray_origin, ray_direction, ray_time)

    def _sample_square(self):
        rand1 = random_double()
        rand2 = random_double()
        return vec3(rand1 - 0.5, rand2 - 0.5, 0)

    def _defocus_disc_sample(self):
        p = random_in_unit_disc()
        return self.center + (self.defocus_disc_u * p[0]) + (self.defocus_disc_v * p[1])
        
    def _ray_color(self, r, depth, world):
        if depth <= 0:
            return color(0, 0, 0)
        
        rec = hit_record(0, vec3(0, 0, 0), 0, 0)
        
        is_hit, rec = world.hit(r, interval(0.001, infinity), rec)
        if not is_hit:
            return self.background
        
        attenuation = color(0, 0, 0)
        scattered = ray(0, 0)
        color_from_emission = rec.mat.emitted(rec.u, rec.v, rec.p)
        
        do_scatter, rec, attenuation, scattered = rec.mat.scatter(r, rec, attenuation, scattered)
        
        if not do_scatter:
            return color_from_emission

        color_from_scatter = self._ray_color(scattered, depth-1, world).mul(attenuation)
        
        return color_from_emission + color_from_scatter
