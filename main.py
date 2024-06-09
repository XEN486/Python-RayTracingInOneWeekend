#from PIL import Image
import sys
import math

from bvh_node import *
from camera import *
from hittable import *
from hittable_list import *
from sphere import *
from material import *
from quad import *

def spheres_scene():
    world = hittable_list()

    ground_material = lambertian(color(0.5, 0.5, 0.5))
    world.add(sphere(point3(0, -1000, 0), 1000, ground_material))

    for a in range(-5, 5):
        for b in range(-5, 5):
            choose_mat = random_double()
            center = point3(a + 0.9 * random_double(), 0.2, b + 0.9 * random_double())
            if ((center - point3(4, 0.2, 0)).length > 0.9):
                sphere_material = None

                if choose_mat < 0.8:
                    albedo = random().mul(random())
                    sphere_material = lambertian(albedo)
                    center2 = center + vec3(0, random_double(0, .5), 0)
                    world.add(sphere(center, 0.2, sphere_material, center2, True))
                elif choose_mat < 0.95:
                    albedo = random(0.5, 1)
                    fuzz = random_double(0, 0.5)
                    sphere_material = metal(albedo, fuzz)
                    world.add(sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = dielectric(1.5)
                    world.add(sphere(center, 0.2, sphere_material))

            material1 = dielectric(1.5)
            world.add(sphere(point3(0,1,0), 1.0, material1))

            material2 = lambertian(color(0.4, 0.2, 0.1))
            world.add(sphere(point3(-4, 1, 0), 1.0, material2))

            material3 = metal(color(0.7, 0.6, 0.5), 0.0)
            world.add(sphere(point3(4, 1, 0), 1.0, material3))

            #world = hittable_list(bvh_node(world))
    
    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_pixel = 10
    cam.max_depth = 8
    cam.background = color(0.7, 0.8, 1.0)

    cam.vfov = 20
    cam.lookfrom = point3(13, 2, 3)
    cam.lookat = point3(0,0,0)
    cam.vup = vec3(0,1,0)

    cam.defocus_angle = 0.6
    cam.focus_dist = 10.0

    return world, cam

def test_scene():
    checker = checker_texture(0.32, color(.2, .3, .1),color(.9, .9, .9))
    ground_material = lambertian(checker)
    albedo = random(0.5, 1)
    fuzz = random_double(0, 1)
    sphere_material = metal(albedo, fuzz)

    sphere_material2 = metal(color(0.7, 0.6, 0.5), 0.0)

    world = hittable_list()
    world.add(sphere(point3(0, 0, -1), 0.5, sphere_material))
    world.add(sphere(point3(0, -100.5, -1), 100, ground_material))
    world.add(sphere(point3(1, 1, -1), 0.75, sphere_material2))

    #world = hittable_list(bvh_node(world))

    cam = camera(aspect_ratio=16.0/9.0, image_width=600, lookfrom=point3(0,0,1), lookat=point3(0,0,0), vup=point3(0,1,0), samples_per_pixel=50)
    cam.background = color(0.7, 0.8, 1.0)
    return world, cam

def checkered_spheres():
    world = hittable_list()

    checker = checker_texture(0.32, color(.2, .3, .1), color(.9, .9, .9))

    world.add(sphere(point3(0, -10, 0), 10, lambertian(checker)))
    world.add(sphere(point3(0, 10, 0), 10, lambertian(checker)))

    cam = camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_pixel = 25
    cam.max_depth = 50
    cam.background = color(0.7, 0.8, 1.0)

    cam.vfov = 20
    cam.lookfrom = point3(13, 2, 3)
    cam.lookat = point3(0,0,0)
    cam.vup = vec3(0,1,0)

    cam.defocus_angle = 0

    return world, cam

def earth():
    earth_texture = image_texture('earthmap.jpg')
    earth_surface = lambertian(earth_texture)
    globe = sphere(point3(0,0,0), 2, earth_surface)

    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_pixel = 10
    cam.max_depth = 8
    cam.background = color(0.7, 0.8, 1.0)

    cam.vfov = 20
    cam.lookfrom = point3(0, 0, 12)
    cam.lookat = point3(0,0,0)
    cam.vup = vec3(0,1,0)

    cam.defocus_angle = 0

    return hittable_list(globe), cam

def perlin_spheres():
    world = hittable_list()

    pertext = noise_texture(4)
    world.add(sphere(point3(0,-1000,0), 1000, lambertian(pertext)))
    world.add(sphere(point3(0,2,0), 2, lambertian(pertext)))

    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_pixel = 10
    cam.max_depth = 8
    cam.background = color(0.7, 0.8, 1.0)
    
    cam.vfov = 20
    cam.lookfrom = point3(13,2,3)
    cam.lookat = point3(0,0,0)
    cam.vup = vec3(0,1,0)

    cam.defocus_angle = 0

    return world, cam

def quads():
    world = hittable_list()

    left_red     = lambertian(color(1.0, 0.2, 0.2))
    back_green   = lambertian(color(0.2, 1.0, 0.2))
    right_blue   = lambertian(color(0.2, 0.2, 1.0))
    upper_orange = lambertian(color(1.0, 0.5, 0.0))
    lower_teal   = lambertian(color(0.2, 0.8, 0.8))

    world.add(quad(point3(-3, -2, 5), vec3(0, 0, -4), vec3(0, 4, 0), left_red))
    world.add(quad(point3(-2, -2, 0), vec3(4, 0, 0), vec3(0, 4, 0), back_green))
    world.add(quad(point3(3, -2, 1), vec3(0, 0, 4), vec3(0, 4, 0), right_blue))
    world.add(quad(point3(-2, 3, 1), vec3(4, 0, 0), vec3(0, 0, 4), upper_orange))
    world.add(quad(point3(-2, -3, 5), vec3(4, 0, 0), vec3(0, 0, -4), lower_teal))

    cam = camera()

    cam.aspect_ratio = 4.0 / 3.0
    cam.image_width = 400
    cam.samples_per_pixel = 10
    cam.max_depth = 8
    cam.background = color(0.7, 0.8, 1.0)

    cam.vfov = 80
    cam.lookfrom = point3(0,0,9)
    cam.lookat = point3(0,0,0)
    cam.vup = vec3(0,1,0)

    cam.defocus_angle = 0

    return world, cam

def simple_light():
    world = hittable_list()

    pertext = noise_texture(4)
    world.add(sphere(point3(0,-1000,0), 1000, lambertian(pertext)))
    world.add(sphere(point3(0, 2, 0), 2, lambertian(pertext)))

    difflight = diffuse_light(color(4,4,4))
    world.add(quad(point3(3,1,-2), vec3(2,0,0), vec3(0,2,0), difflight))
    world.add(sphere(point3(0,7,0), 2, difflight))

    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_pixel = 10
    cam.max_depth = 50
    cam.background = color(0,0,0)
    
    cam.vfov = 20
    cam.lookfrom = point3(26,3,6)
    cam.lookat = point3(0,2,0)
    cam.vup = vec3(0,1,0)

    cam.defocus_angle = 0

    return world, cam

def cornell_box():
    world = hittable_list()

    red = lambertian(color(.65, .05, .05))
    white = lambertian(color(.73, .73, .73))
    green = lambertian(color(.12, .45, .15))
    light = diffuse_light(color(15, 15, 15))

    world.add(quad(point3(555,0,0), vec3(0,555,0), vec3(0,0,555), green))
    world.add(quad(point3(0,0,0), vec3(0,555,0), vec3(0,0,555), red))
    #world.add(quad(point3(113, 554, 127), vec3(330, 0, 0), vec3(0,0,305), light))
    world.add(quad(point3(343, 554, 332), vec3(-130, 0, 0), vec3(0,0,-105), light))
    world.add(quad(point3(0,0,0), vec3(555,0,0), vec3(0,0,555), white))
    world.add(quad(point3(555,555,555), vec3(-555, 0, 0), vec3(0,0,-555), white))
    world.add(quad(point3(0,0,555), vec3(555,0,0), vec3(0,555,0), white))

    world.add(box(point3(130, 0, 65), point3(295, 165, 230), white))
    world.add(box(point3(265, 0, 295), point3(430, 330, 460), white))

    cam = camera()
    cam.aspect_ratio = 1.0
    cam.image_width = 400
    cam.samples_per_pixel = 50
    cam.max_depth = 50
    cam.background = color(0,0,0)

    cam.vfov = 40
    cam.lookfrom = point3(278, 278, -800)
    cam.lookat = point3(278, 278, 0)
    cam.vup = vec3(0,1,0)

    cam.defocus_angle = 0

    return world, cam    
    
def main():
    world, cam = cornell_box()

    cam.render(world)
    #Image.open('image.ppm').show()

if __name__ == '__main__':
    main()
