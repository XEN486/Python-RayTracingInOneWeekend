#from PIL import Image
import sys
import math

from bvh_node import *
from camera import *
from constant_medium import *
from hittable import *
from hittable_list import *
from sphere import *
from material import *
from quad import *
from vector import *

def spheres_scene():
    world = hittable_list()

    checker = checker_texture(0.32, color(.2, .3, .1), color(.9, .9, .9))
    ground_material = lambertian(checker) # color(0.5,0.5,0.5)
    world.add(sphere(point3(0, -1000, 0), 1000, ground_material))

    for a in range(-4, 4):
        for b in range(-4, 4):
            choose_mat = random_double()
            center = point3(a + 0.9 * random_double(), 0.2, b + 0.9 * random_double())
            if ((center - point3(4, 0.2, 0)).length > 0.9):
                sphere_material = None

                if choose_mat < 0.8:
                    albedo = random().mul(random())
                    sphere_material = lambertian(albedo)
                    world.add(sphere(center, 0.2, sphere_material))
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

            world = hittable_list(bvh_node(world))
    
    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 1200
    cam.samples_per_pixel = 50
    cam.max_depth = 50
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
    cam.samples_per_pixel = 1
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
    #light = diffuse_light(color(15, 15, 15))
    light = diffuse_light(color(7, 7, 7))
    
    world.add(quad(point3(555,0,0), vec3(0,555,0), vec3(0,0,555), green))
    world.add(quad(point3(0,0,0), vec3(0,555,0), vec3(0,0,555), red))
    world.add(quad(point3(113, 554, 127), vec3(330, 0, 0), vec3(0,0,305), light))
    #world.add(quad(point3(343, 554, 332), vec3(-130, 0, 0), vec3(0,0,-105), light))
    world.add(quad(point3(0,0,0), vec3(555,0,0), vec3(0,0,555), white))
    world.add(quad(point3(555,555,555), vec3(-555, 0, 0), vec3(0,0,-555), white))
    world.add(quad(point3(0,0,555), vec3(555,0,0), vec3(0,555,0), white))
    
    box1 = box(point3(0,0,0), point3(165, 330, 165), green)
    box1 = rotate_y(box1, 15)
    box1 = translate(box1, vec3(265, 0, 295))
    world.add(box1)

    box2 = box(point3(0,0,0), point3(165, 165, 165), green)
    box2 = rotate_y(box2, -18)
    box2 = translate(box2, vec3(130, 0, 65))
    world.add(box2)

    world = hittable_list(bvh_node(world))

    cam = camera()
    cam.aspect_ratio = 1.0
    cam.image_width = 200
    cam.samples_per_pixel = 50
    cam.max_depth = 50
    cam.background = color(0,0,0)

    cam.vfov = 40
    cam.lookfrom = point3(278, 278, -800)
    cam.lookat = point3(278, 278, 0)
    cam.vup = vec3(0,1,0)

    cam.defocus_angle = 0

    return world, cam    

def cornell_smoke():
    world = hittable_list()
    
    red = lambertian(color(.65, .05, .05))
    white = lambertian(color(.73, .73, .73))
    green = lambertian(color(.12, .45, .15))
    light = diffuse_light(color(7, 7, 7))

    world.add(quad(point3(555,0,0), vec3(0,555,0), vec3(0,0,555), green))
    world.add(quad(point3(0,0,0), vec3(0,555,0), vec3(0,0,555), red))
    world.add(quad(point3(113,554,127), vec3(330,0,0), vec3(0,0,305), light))
    world.add(quad(point3(0,555,0), vec3(555,0,0), vec3(0,0,555), white))
    world.add(quad(point3(0,0,0), vec3(555,0,0), vec3(0,0,555), white))
    world.add(quad(point3(0,0,555), vec3(555,0,0), vec3(0,555,0), white))

    box1 = box(point3(0,0,0), point3(165,330,165), white)
    box1 = rotate_y(box1, 15)
    box1 = translate(box1, vec3(265,0,295))

    box2 = box(point3(0,0,0), point3(165,165,165), white)
    box2 = rotate_y(box2, -18)
    box2 = translate(box2, vec3(130,0,65))

    world.add(constant_medium(box1, 0.01, color(0,0,0)))
    world.add(constant_medium(box2, 0.01, color(1,1,1)))

    world = hittable_list(bvh_node(world))

    cam = camera()
    cam.aspect_ratio = 1.0
    cam.image_width = 200
    cam.samples_per_pixel = 50
    cam.max_depth = 50
    cam.background = color(0,0,0)

    cam.vfov = 40
    cam.lookfrom = point3(278, 278, -800)
    cam.lookat = point3(278, 278, 0)
    cam.vup = vec3(0,1,0)

    cam.defocus_angle = 0

    return world, cam

def final_scene(image_width, samples_per_pixel, max_depth):
    boxes1 = hittable_list()
    ground = lambertian(color(0.48, 0.83, 0.53))

    boxes_per_side = 20
    for i in range(boxes_per_side):
        for j in range(boxes_per_side):
            w = 100
            x0 = -1000 + i*w
            z0 = -1000 + j*w
            y0 = 0
            x1 = x0 + w
            y1 = random_double(1, 101)
            z1 = z0 + w

            boxes1.add(box(point3(x0,y0,z0), point3(x1,y1,z1), ground))

    world = hittable_list()
    world.add(bvh_node(boxes1))

    light = diffuse_light(color(7, 7, 7))
    world.add(quad(point3(123,554,147), vec3(300,0,0), vec3(0,0,265), light))

    center1 = point3(400, 400, 200)
    center2 = center1 + vec3(30,0,0)
    sphere_material = lambertian(color(0.7, 0.3, 0.1))
    world.add(sphere(center1, 50, sphere_material, center2, True))

    world.add(sphere(point3(260, 150, 45), 50, dielectric(1.5)))
    world.add(sphere(
        point3(0, 150, 145), 50, metal(color(0.8, 0.8, 0.9), 1.0)
    ))

    boundary = sphere(point3(360,150,145), 70, dielectric(1.5))
    world.add(boundary)
    world.add(constant_medium(boundary, 0.2, color(0.2, 0.4, 0.9)))
    boundary = sphere(point3(0,0,0), 5000, dielectric(1.5))
    world.add(constant_medium(boundary, .0001, color(1,1,1)))

    emat = lambertian(image_texture('earthmap.jpg'))
    world.add(sphere(point3(400,200,400), 100, emat))
    pertext = noise_texture(0.2)
    world.add(sphere(point3(220,280,300), 80, lambertian(pertext)))

    boxes2 = hittable_list()
    white = lambertian(color(.73, .73, .73))
    ns = 1000
    for j in range(ns):
        boxes2.add(sphere(random(0,165), 10, white))

    world.add(translate(rotate_y(bvh_node(boxes2), 15), vec3(-100,270,395)))

    cam = camera()

    cam.aspect_ratio = 1.0
    cam.image_width = image_width
    cam.samples_per_pixel = samples_per_pixel
    cam.max_depth = max_depth
    cam.background = color(0,0,0)

    cam.vfov = 40
    cam.lookfrom = point3(478, 278, -600)
    cam.lookat = point3(278, 278, 0)
    cam.vup = vec3(0,1,0)

    cam.defocus_angle = 0

    return world, cam

def main():
    world, cam = final_scene(400, 250, 4)

    print('gooby')
    cam.render(world)
    #Image.open('image.ppm').show()

if __name__ == '__main__':
    main()
